import pandas as pd
import numpy as np
import io
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 1. Processamento e Preparação dos Dados ---
def process_data(file_path):
    """Lê o arquivo de dados, extrai todos os quadros de tempo e seus dados."""
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return []

    # Regex para encontrar seções de tempo e dados (funciona para o novo formato)
    pattern = re.compile(r'# Tempo =\s*([0-9\.Ee\-\+]+)\s*\n(.*?)(?=# Tempo = |\Z)', re.DOTALL)
    all_data = []
    matches = pattern.findall(content)

    if not matches:
        print("Aviso: Nenhuma marcação '# Tempo = ...' encontrada. Verifique o formato do arquivo.")
        return []

    for time_str, data_block in matches:
        time_value = float(time_str)
        data_io = io.StringIO(data_block)
        
        try:
            # Lê os dados em duas colunas, separadas por espaços
            df_temp = pd.read_csv(data_io, sep='\s+', skipinitialspace=True, 
                                  header=None, comment='#', engine='python')
            
            if df_temp.shape[1] >= 2:
                # Usa as duas primeiras colunas e garante que são numéricas
                df_temp = df_temp.iloc[:, :2].dropna(how='all')
                df_temp.iloc[:, 0] = pd.to_numeric(df_temp.iloc[:, 0], errors='coerce')
                df_temp.iloc[:, 1] = pd.to_numeric(df_temp.iloc[:, 1], errors='coerce')
                df_temp = df_temp.dropna()
                
                if not df_temp.empty:
                    df_temp.columns = ['Posicao', 'Deslocamento']
                    df_temp['Tempo'] = time_value
                    all_data.append(df_temp)
            
        except Exception as e:
            # print(f"Erro ao processar bloco de tempo {time_value}: {e}")
            continue
    
    return all_data

# --- 2. Geração da Animação ---
def create_animation(processed_data, gif_filename="simulacao_onda_elastica.gif"):
    """Cria e salva a animação GIF a partir dos dados processados."""
    if not processed_data:
        return

    # Encontra os limites globais para garantir que o eixo não flutue
    x_min = min(df['Posicao'].min() for df in processed_data)
    x_max = max(df['Posicao'].max() for df in processed_data)
    y_max = max(df['Deslocamento'].abs().max() for df in processed_data if not df.empty) * 10 
    
    # Configuração do Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    line, = ax.plot([], [], lw=2, color='b')
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-y_max, y_max)
    ax.set_xlabel("Posição (x)")
    ax.set_ylabel("Deslocamento (u)")
    ax.set_title("Simulação de Onda em Barra Elástica")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.axhline(0, color='gray', linestyle='-', linewidth=0.5)
    
    time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes) # Exibe o tempo
    
    # Função de inicialização
    def init():
        line.set_data([], [])
        time_text.set_text('')
        return line, time_text

    # Função de atualização (frame)
    def update(frame_index):
        df_frame = processed_data[frame_index]
        time = df_frame['Tempo'].iloc[0]
        
        line.set_data(df_frame['Posicao'], df_frame['Deslocamento'])
        time_text.set_text(f'Tempo = {time:.6f} s')
        
        return line, time_text

    # Usaremos todos os quadros (30) no seu caso, com intervalo de 100ms
    total_frames = len(processed_data)
    frame_indices = np.arange(0, total_frames, 1)
    interval_ms = 25 
    
    print(f"Salvando o GIF com {total_frames} quadros (10 quadros/s). Aguarde...")

    anim = FuncAnimation(fig, update, frames=frame_indices, init_func=init, blit=True, interval=interval_ms, repeat=True)

    try:
        # Tenta salvar o GIF usando o writer 'pillow' (o mais comum)
        anim.save(gif_filename, writer='pillow', fps=1000/interval_ms)
        plt.close(fig) 
        print(f"GIF salvo com sucesso como: {gif_filename}")
    except Exception as e:
        plt.close(fig) 
        print(f"\n--- ERRO AO SALVAR O GIF ---")
        print(f"Erro: {e}")
        print("Certifique-se de ter a biblioteca 'Pillow' (ou 'imagemagick') instalada.")
        print("Você pode instalá-la com: pip install Pillow")

# --- Execução Principal ---
if __name__ == '__main__':
    data = process_data("resultados.dat")
    if data:
        create_animation(data)
    else:
        print("Falha na execução. Não foi possível gerar a animação. Verifique a saída do processamento.")