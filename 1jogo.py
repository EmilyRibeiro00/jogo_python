import pygame
from pygame.locals import *      #Importa constantes e eventos do Pygame para facilitar o uso no código.
from random import randint
from sys import exit  

#Inicializaçao 
pygame.init()

#Cores - valores RGB 
cinza = (100,100,100)
verde = (76,208,56)
branco = (255,255,255)
preto = (0,0,0)

#Configurações do jogo
game_over = False
imagem_GameOver = pygame.image.load('game_over.png')
velocidade = 2  #variavel para ter maior controle da incrementaçao no eixo Y
max_velocidade = 10
aceleracao = 0.001

#Tela
altura_tela = 500
largura_tela = 500
tela = pygame.display.set_mode((largura_tela,altura_tela))
pygame.display.set_caption('Jogo de Corrida')

#Desenhando o fundo 
rua = (100,0,300,altura_tela)
lado_esquerdo_da_tela = (95,0,10,altura_tela) #Tupla = (coord. X, coord. Y, largura do retangulo, altura do retangulo)
lado_direito_da_tela = (395,0,10,altura_tela)

#Árvore
arvore = pygame.image.load("arvore.png") 
posicoes_arvores = [(25,0), (25, 125), (25, 250), (25,375), (430,0), (430, 125), (430, 250),(430,375)] #Lista de truplas

#Faixas da pista
pista_esquerda = 150 #Posiçao do inicio da pista no eixo X 
pista_central = 250
largura_faixa = 10
altura_faixa = 50
movimento_da_pista = 0

#Áudios
musica_jogo = pygame.mixer.Sound('musica_jogo_rodando.mp3')
musica_jogo.play(-1)
som_colisao = pygame.mixer.Sound('Som_colisao.wav')
som_game_over = pygame.mixer.Sound('musica_GameOver.wav')

#Carros
carro_jogador = pygame.image.load('carro_jogador.png')
X_carro_jogador = 220
Y_carro_jogador = 400
moto = pygame.image.load('moto.png')
X_moto = 130
Y_moto = 420
carro_preto = pygame.image.load('carro_preto.png')
X_carro_preto = 330
Y_carro_preto = 350
carro_amarelo = pygame.image.load('carro_amarelo.png')
X_carro_amarelo = 225
Y_carro_amarelo = 0

velocidade_outros_carros = 5

# Tela de game over
fonte_GameOver = pygame.font.Font(None, 36) #Fonte principal Game Over
gameOver_Texto = fonte_GameOver.render("Pressione espaço para continuar...",False, preto) #Texto de game over
gameOver_Texto_posicao = (50,300)

#Texto de score
fonteScore = pygame.font.Font(None, 25) #Fonte principal Score
time_score = 0
score = 0
score_Texto = fonteScore.render("Pontos: " + str(score), True, branco) #True = "suaviza" a letra 
score_Posicao = (largura_tela-90,10)

#Tela de menu
imagem_menu = pygame.image.load('imagem_menu.jpg')
fonte_menu = pygame.font.Font(None, 30)
texto_menu = fonte_menu.render('Pressione espaço para iniciar',True,preto) 
posicao_texto_menu = (100,450)


    

#=============================================================================================================================#

#Loop principal
jogo_rodando = True
menu_inicial = True
clock = pygame.time.Clock()

while jogo_rodando:

    if menu_inicial:

        # Lógica do menu inicial
        for event in pygame.event.get():  #inicia um loop para obter todos os eventos do pygame que ocorreram desde a última iteração do loop principal
            if event.type == QUIT:
                jogo_rodando = False
                menu_inicial = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    menu_inicial = False
        
        tela.fill(branco)
        tela.blit(imagem_menu, (0, 0))
        tela.blit(texto_menu,posicao_texto_menu)
        pygame.display.update()


    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                jogo_rodando = False
            

        #Movimentaçao do carro do jogador
        comando = pygame.key.get_pressed()
        if comando[pygame.K_LEFT]:
            if X_carro_jogador > 100:
                X_carro_jogador -= 5
        if comando[pygame.K_RIGHT]:
            if X_carro_jogador < 345:
                X_carro_jogador += 5
        if comando[pygame.K_UP]:
            if Y_carro_jogador > 0:
                Y_carro_jogador -= 5
        if comando[pygame.K_DOWN]:
            if Y_carro_jogador < 400:
                Y_carro_jogador += 5

        grama = tela.fill(verde) #Grama
    

        #Desenhando a avenida
        pygame.draw.rect(tela,cinza,rua) #Rua
        pygame.draw.rect(tela,branco,lado_esquerdo_da_tela) #Canteiro esquerdo
        pygame.draw.rect(tela,branco,lado_direito_da_tela) #Canteiro direito


        #Movimento árvores e faixas
        movimento_da_pista += velocidade * 2
        if movimento_da_pista >= altura_faixa * 2:
            movimento_da_pista = 0
        for i, posicao in enumerate(posicoes_arvores):
            posicoes_arvores[i] = (posicao[0], (posicao[1] + velocidade * 2) % altura_tela)
        for posicao in posicoes_arvores:
            tela.blit(arvore, posicao)


        for posicao_eixoY in range(altura_faixa * -2, altura_tela, altura_faixa * 2):
            pygame.draw.rect(tela, branco, (pista_esquerda + 45, posicao_eixoY + movimento_da_pista, largura_faixa, altura_faixa))  #45 = largura da pista
            pygame.draw.rect(tela, branco, (pista_central + 45, posicao_eixoY + movimento_da_pista, largura_faixa, altura_faixa))
        

        #Carros
        tela.blit(carro_jogador,(X_carro_jogador,Y_carro_jogador))
        tela.blit(moto,(X_moto,Y_moto))
        tela.blit(carro_preto, (X_carro_preto,Y_carro_preto))
        tela.blit(carro_amarelo, (X_carro_amarelo,Y_carro_amarelo))
        tela.blit(score_Texto,score_Posicao)
        

        #Aqui criamos um if para o score nao correr muito rápido
        if time_score < 50:
            time_score += 1
        else:
            score += 1
            time_score = 0
            
        score_Texto = fonteScore.render("Pontos: " + str(score), True, preto) 
        

        #Movimentaçao dos outros carros
        Y_carro_amarelo += velocidade_outros_carros + 2 #incremetando o eixo Y do carro
        if Y_carro_amarelo >= 500:
            Y_carro_amarelo = randint(-1000,0) #reiniciando o carro em uma posiçao aleatoria no eixo Y fora da tela
        Y_carro_preto += velocidade_outros_carros + 3 
        if Y_carro_preto >= 500:
            Y_carro_preto = randint(-2000,0)
        Y_moto += velocidade_outros_carros + 2 
        if Y_moto >=500:
            Y_moto = randint(-2000,0)


        # Aumenta gradualmente a velocidade
        if velocidade < max_velocidade:
            velocidade += aceleracao
            velocidade_outros_carros += aceleracao


        #Colisao
        size_carro_jogador= pygame.Rect((X_carro_jogador,Y_carro_jogador), carro_jogador.get_size())
        size_carro_amarelo= pygame.Rect((X_carro_amarelo,Y_carro_amarelo), carro_amarelo.get_size())
        size_carro_preto= pygame.Rect((X_carro_preto,Y_carro_preto), carro_preto.get_size())
        size_moto= pygame.Rect((X_moto,Y_moto), moto.get_size())


        #Tela de Game Over
        if size_carro_jogador.colliderect(size_carro_amarelo) or size_carro_jogador.colliderect(size_carro_preto) or size_carro_jogador.colliderect(size_moto):
            musica_jogo.stop()
            som_colisao.play()
            pygame.time.delay(500)
            som_colisao.stop()
            gameOverSound = True 
            game_over = True

        #Tela de Game Over
        if game_over:
            tela.fill(branco)
            tela.blit(imagem_GameOver, (-20, 0))
            tela.blit(gameOver_Texto,gameOver_Texto_posicao)

            #total_pontos = fonte_GameOver.render(score_Texto,True, preto) #Texto de pontos finais
            total_pontos_Texto_posicao = (205,355)

            tela.blit(score_Texto,total_pontos_Texto_posicao)
            pygame.display.update()
            
            if gameOverSound:
                som_game_over.play()
                pygame.time.delay(1000)
                som_game_over.stop()
                gameOverSound=False


        
        pygame.display.update()
        
        

        #Laço de repetiçao enquanto (game over == True)
        while game_over:

            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    jogo_rodando=False
                    game_over=False
                
                #Reset do jogo. Todas as posicoes voltam ao original
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        musica_jogo.play(-1)
                        X_carro_jogador = 220
                        Y_carro_jogador = 400
                        X_moto = 120
                        Y_moto = 420
                        X_carro_preto = 320
                        Y_carro_preto = 350
                        X_carro_amarelo = 230
                        Y_carro_amarelo = 0
                        score = 0
                        velocidade = 2
                        game_over= False

            

        
        clock.tick(60)  #chamada de função que controla a taxa de quadros por segundo (FPS) do jogo


#Encerramento 
pygame.quit()