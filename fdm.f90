! ==================================================================
! Algoritmo desenvolvido por Felipe Diogo M. Silva
! Objetivo	: Aprender fortran e aplicar conhecimentos para 
! 			  uma atividade de Tópicos Especiais em Vibrações
! Data		: 25/10/2025
! ==================================================================

program diferencasFinitas
implicit none

	! ==================================================================
    ! definições do algoritmo ( variáveis, parâmetros e tipos
    ! ==================================================================

    integer, parameter :: dp = kind(1.0d0)
    real(dp), allocatable, dimension(:,:) :: u
    integer :: N = 250, nt, i, j
    real(dp) :: xi=0.0_dp, xf=1.0_dp, dx, dt, v0=0.5_dp, t=1.0_dp
    real(dp) :: cfl=0.5_dp, rho=2700.0_dp, E=70e9_dp, c
    
	! ================================================================== 
    ! preparação para a simulação
    ! ==================================================================
	
    ! Cálculos na ordem CORRETA
    dx = (xf-xi) / (N - 1) 			! tamanho todo / número de divisões = tamanho do meu diferencial de espaço
    c = sqrt(E/rho)  				! velocidade de onda no material
    dt = dx*sqrt(cfl/c) 			! definindo o time step para uma simulação estável
    cfl = c * (dt**2) / (dx**2)  	! recalculado o cfl a partir do dt calculado
    nt = int(t/dt)   				! converter para inteiro
		
	! ==================================================================
    ! preparação para salvar os dados e descrever o programa
    ! ==================================================================
	
	open(unit=10, file='resultados.dat', status='replace')
	write(10, *) " Simulação de Onda - Barra Elástica"
	write(10, *) " dx = ", dx, " dt = ", dt, " CFL = ", cfl
	write(10, *) " N = ", N, " nt = ", nt
	write(10, *) " Colunas: Posição Deslocamento"
	
	! Alocando um pedaço de memória do tamanhho u(nt, N)
    allocate(u(nt, N))
    u = 0.0_dp ! inicializando tudo pra a matriz não ficar vazia
   	
	! inicializando
	u(1, :) = 0.0_dp  ! no tempo 0, tudo ta parado
	u(:, 1) = 0.0_dp  ! o engaste, para qualquer tempo, tá parado
	
	! ==================================================================
	! calculando o primeiro passo i=1 (o primeiro passo é uma exceção)
	! ==================================================================
	
	print *, "=== EXECUTANDO PRIMEIRO PASSO (i=1) ==="
	do j = 2, N-1
		u(2, j) = (cfl*u(1, j-1) + (2.0_dp - 2.0_dp*cfl)*u(1, j) + cfl*u(1, j+1)) / 2.0_dp ! u{1, 2:n-1} do caderno
	end do
	
		u(2, N) = (2*cfl*u(1, N-1) + (2.0_dp - 2.0_dp*cfl)*u(1, N) + 2*dt*v0) / 2.0_dp  	! aplicação do impulso na ponta
	
	print *, "u(2,1)  = ", u(2,1), " (engaste)"
    print *, "u(2,N/2) = ", u(2,N/2), " (ponto central)"
    print *, "u(2,N)  = ", u(2,N), " (extremidade com impulso)"
	
	! ==================================================================
	! calculando do passo i=2 pra frente (loop principal)
	! ==================================================================
	
    print *, "=== INICIANDO LOOP PRINCIPAL ==="
	
	do i = 2, nt-1
		do j = 2, N-1
		
			! do tempo imediatamente após o impulso ao fim e do ponto após o engaste
			! até o penúltimo
			
			u(i+1, j) = cfl*u(i, j-1) + (2.0_dp - 2.0_dp*cfl)*u(i, j) + &
						cfl*u(i, j+1) - u(i-1, j) ! loop principal do meio no caderno 
		end do
		
			! todos os tempos para o último ponto (na ponta)
			u(i+1, N) = 2*cfl*u(i, N-1) + (2.0_dp - 2.0_dp*cfl)*u(i, N) - u(i-1, N)
		
	! ==================================================================
	! escrevendo os resultados (arquivo .dat)
	! ==================================================================		
	
		! mod = módulo/resto de uma divisão, ou seja, se o número for divisível
		! por 50 (sobrar 0), vou escrever o resultado eg.: (100, 150, 200...)
		! para burros: a cada 50 iterações, eu escrevo o rsultado
		
		if (mod(i, 100) == 0) then
			write(10, *) "# Tempo = ", (i+1)*dt
				do j = 1, N
					write(10, *) (j-1)*dx, u(i+1, j)
				end do
			write(10, *)  ! Linha vazia para gnuplot
			print *, "Salvo: tempo = ", (i+1)*dt, "s"
		end if
		
	end do
	
	! fechando o arquivo dat que tá aberto escrevendo resultados
	close(10)
	print *, "Dados salvos em 'resultados.dat'"
    
end program diferencasFinitas