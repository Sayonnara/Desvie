import pygame
import random

# Inicializar o pygame
pygame.init()

# Configurações da tela
largura, altura = 500, 500
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo com Cronômetro e Tela Inicial")

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)

# Fonte para o cronômetro e mensagens
fonte = pygame.font.Font(None, 36)

# Jogador
jogador_tam = 50
jogador_x, jogador_y = largura // 2, altura - jogador_tam - 10
velocidade = 5

# Obstáculo
obstaculo_largura = 50
obstaculo_altura = 20
obstaculo_x = random.randint(0, largura - obstaculo_largura)
obstaculo_y = -obstaculo_altura
obstaculo_velocidade = 5

# Variáveis de controle
relogio = pygame.time.Clock()
jogo_ativo = False  # Para controlar se o jogo está rodando
jogando = True  # Para controlar o loop principal
tempo_final = None  # Variável para armazenar o tempo final ao fim do jogo

# Função para mostrar a tela inicial
def mostrar_tela_inicial():
    tela.fill(BRANCO)
    texto_inicio = fonte.render("Pressione ESPAÇO para começar o jogo", True, PRETO)
    tela.blit(texto_inicio, (largura // 2 - texto_inicio.get_width() // 2, altura // 2 - 50))
    pygame.display.update()

# Função para mostrar a mensagem de fim de jogo
def mostrar_fim_jogo(tempo_final):
    tela.fill(BRANCO)
    texto_fim = fonte.render(f"Fim de Jogo! Tempo: {tempo_final}s", True, PRETO)
    reiniciar_texto = fonte.render("Pressione 'R' para reiniciar ou 'S' para sair", True, PRETO)
    tela.blit(texto_fim, (largura // 2 - texto_fim.get_width() // 2, altura // 2 - 50))
    tela.blit(reiniciar_texto, (largura // 2 - reiniciar_texto.get_width() // 2, altura // 2 + 20))
    pygame.display.update()

# Loop principal
while jogando:
    if not jogo_ativo:
        mostrar_tela_inicial()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                jogo_ativo = True  # Começar o jogo
                jogador_x = largura // 2
                obstaculo_y = -obstaculo_altura
                tempo_inicial = pygame.time.get_ticks()  # Marcar o início do jogo
                tempo_final = None  # Resetar o tempo final ao reiniciar
    else:
        # Preencher a tela com a cor branca
        tela.fill(BRANCO)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogando = False

        # Controle do jogador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jogador_x > 0:
            jogador_x -= velocidade
        if teclas[pygame.K_RIGHT] and jogador_x < largura - jogador_tam:
            jogador_x += velocidade

        # Movimento do obstáculo
        obstaculo_y += obstaculo_velocidade
        if obstaculo_y > altura:
            obstaculo_y = -obstaculo_altura
            obstaculo_x = random.randint(0, largura - obstaculo_largura)

        # Colisão
        jogador_rect = pygame.Rect(jogador_x, jogador_y, jogador_tam, jogador_tam)
        obstaculo_rect = pygame.Rect(obstaculo_x, obstaculo_y, obstaculo_largura, obstaculo_altura)
        if jogador_rect.colliderect(obstaculo_rect):
            tempo_final = (pygame.time.get_ticks() - tempo_inicial) // 1000
            jogo_ativo = False

        # Desenho dos retângulos (jogador e obstáculo)
        pygame.draw.rect(tela, AZUL, jogador_rect)
        pygame.draw.rect(tela, VERMELHO, obstaculo_rect)

        # Calcular o tempo decorrido em segundos
        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicial) // 1000
        texto_tempo = fonte.render(f"Tempo: {tempo_decorrido}s", True, PRETO)
        tela.blit(texto_tempo, (10, 10))

        # Atualizar a tela
        pygame.display.update()
        relogio.tick(30)
    
    # Mostrar a mensagem de fim de jogo e esperar o jogador escolher
    if not jogo_ativo and jogando and tempo_final is not None:
        mostrar_fim_jogo(tempo_final)
        esperando_resposta = True
        while esperando_resposta:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jogando = False
                    esperando_resposta = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        jogo_ativo = True  # Reiniciar o jogo
                        jogador_x = largura // 2
                        obstaculo_y = -obstaculo_altura
                        tempo_inicial = pygame.time.get_ticks()  # Marcar o reinício do jogo
                        esperando_resposta = False
                    elif evento.key == pygame.K_s:
                        jogando = False
                        esperando_resposta = False

# Encerrar o pygame
pygame.quit()
