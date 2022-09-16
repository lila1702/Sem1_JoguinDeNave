import pygame
import math
from pygame.locals import *  # Importanto do submodulo locals, dentro da biblioteca do pygame, todas as funções e constantes
from sys import \
    exit  # Importanto da biblioteca sys, originária do python, uma função responsável pelo fechamneto da janela do jogo
from random import randint
from random import uniform
from random import choice



# Inicilaizando todas as funções e comandos do pygame.
pygame.init()  

# Definindo variáveis
largura = 860
altura = 620

# Variavel/lista de mensagens de game over
referencias = [
    ' Não Desista Agora, Tenha DETERMINAÇÃO',
    'jogador? JOGADOR?! JOGADOOOOOOOOOOR!',
    '                    WASTED!',
    '               VOCÊ MORREU  ',
    '               MISSON FAILED',
    '                   TOO BAD...',
    '             Você é Muito Lento',
    'Insert a Coin to ... oh Wait No Continue'
    ]

# Variáveis do jogador
# Variável criada para inserir uma imagem em cima do quadrado desenhado anteriormente.
jogadorImg = pygame.transform.scale(pygame.image.load("Player_Nave.png"),(64,64))
# Variável que guarda a posição do jogador no eixo x.
xdojogador = largura / 2
# Variável que guarda a posição do jogador no eixo y.
ydojogador = altura - 52
# Variável para atualização do x do jogador na reta.
atua_xdoj = 0

# Função para desenhar o player na tela
def jogador(x,y):
    tela.blit(jogadorImg, (x, y))


# variáveis de controle de balas

count = 0
municao = []
gatilho = False

# Função dos Tiros
def atirar(balas):
    global gatilho # se o gatilho tiver pronto para atirar, a função pode ser utilizada

    if gatilho:
        balas.append(pygame.Rect(xdojogador + 32, ydojogador + 20, 3, 17)) # adcionasse uma nova bala a lista de munições
        gatilho = False # e desativa o gatinho

    for bala in balas: # checagem de bala em bala em toda a munição
        bala.y -= 10
        pygame.draw.rect(tela, (255, 0, 0), bala)

    for index, bala in enumerate(balas): # laço destruidor de balas que checa qual bala tá em qual index e ...
        if bala.y <= 0:
            del balas[index]  # ... quando passa da tela a destroi da lista.

    return balas # atualizando a lista de munição pra cada tic


# Variáveis dos Inimigos
inimigosImgs = {
    1 : pygame.transform.scale(pygame.image.load("Inimigo1_Nave.png"),(50,50)),
    2 : pygame.transform.scale(pygame.image.load("Inimigo2_Nave.png"),(40,40))
} # Dicionário com todas os sprites para os inimigos

inimigoImg = inimigosImgs[randint(1, 2)] # Inicializa o sprite da primeira horda aleatoriamente
horda = [] # Útil pro spawn
kills = 0 # Contagem de mortes inimigas

# Controle de spawn dos inimigos
maximo = 0 # Útil pro spawn
controle = 0 # Útil pro spawn

# Funções dos Inimigos
""" A colisão em nosso jogo utiliza-se da distância entre dois pontos em um plano cartesiano
    como parâmetro de processamento se um projétil acertou ou não o inimigo. 
    No caso, se a distância entre os dois for menos que 20 pixels significa que o alvo foi acertado."""
def colisao(inimigox, inimigoy, tirox, tiroy):
    distancia_bala_inimigo = math.sqrt(math.pow((inimigox - tirox), 2) + math.pow((inimigoy - tiroy), 2))
    if distancia_bala_inimigo < 20:
        return True
    else:
        return False

def SpawnInimigos(inimigos):
    global inimigoImg
    global controle
    global maximo
    global pontos
    global kills
    
    # Vê quantos inimigos restantes há na horda atual
    restante = len(inimigos)
    # Gera uma posição X aleatória dentro da tela para o spawn dos inimigos
    posSpawnX = randint(15, largura - 30)
    
    # Spawnará os inimigos mais e mais perto um do outro, dependendo das kills
    if (kills <= 10):
        posSpawnY = uniform(-550, -1500)
    elif (kills > 10 and kills <= 25):
        posSpawnY = uniform(-550, -940)
    elif (kills > 25):
        posSpawnY = uniform(-200, -600)
    
    # Se não tiver nenhum inimigo restante...
    if (restante == 0):
        # Aumentará o máximo de inimigos da horda
        maximo = 1 + controle
        # E acrescentará mais um no contador de quantas hordas passaram
        controle += 1 # Assim como já deixará encaminhado o valor de inimigos da próxima horda.
        # Gerará um novo sprite pra nova horda
        inimigoImg = inimigosImgs[randint(1, 2)]
    
    # Irá acrescentar o(s) inimigo(s) em si para a lista da horda.
    # Envia um Rect (Retângulo) pois o sprite do inimigo fica por cima dele.
    if (maximo > 0):
        inimigos.append(pygame.Rect(posSpawnX, posSpawnY, 20, 20))
    
    for inimigo in inimigos:
        # Nunca deixará ter mais que 20 inimigos na tela de uma vez.
        if (restante <= 20):
                inimigo.y += 3 # Move o inimigo
                tela.blit(inimigoImg, (inimigo.x-10,inimigo.y-2)) # Desenha ele na tela
    
    # Verifica todos os inimigos na lista por índice.
    for index, inimigo in enumerate(inimigos):
        # Se o inimigo chegar embaixo da tela, atrás do player, aquele inimigo será deletado.
        # Além disso, também irá remover um ponto de vida do player.
        if (inimigo.y >= altura - 20):
            if (pontos != 0):
                pontos -= 1
            del inimigos[index]
            
    # Irá diminuir o máximo de inimigos da horda atual a cada um que for destruído
    # ou chegar no final, assim fazendo com que eles não respawnem.
    maximo = maximo - 1
    # Retorna a horda atualizada
    return inimigos

# Pontuação de vida
pontos = 10

# retangulo de interação do menu
xi = 270
yi = 260
intera = 0

#temporiazador dos créditos
run_creditos_tutoriais = False

# Esconde o ponteiro do mouse na janela do jogo.
pygame.mouse.set_visible(False)

# Mostra a tela do jogo com o submodulo display. Recebe como parâmetros largura e altura.
tela = pygame.display.set_mode((largura, altura))
# Definirá o nome da janela aberta para o jogo com o set_caption.
pygame.display.set_caption("Jogin d'navyie")

# Definição das fontes usadas por todo o jogo.
#Parâmetros em ordem: Fonte, tamanho, negrito, itálico.
fonte = pygame.font.SysFont("Arial", 30, False, False)
fonte_hud = pygame.font.SysFont(("EX Comic Sans"), (100))
fonte_menu = pygame.font.SysFont(("EX Comic Sans"), (80))

# Controla os frames por segundo a partir da função clock do módulo time.
relogio = pygame.time.Clock()

# Guarda o gráfico do cenário na variável fundo.
fundo = pygame.transform.scale(pygame.image.load("estrelas.jpg"), (largura, altura))

# função de crédito dos autores :D
def creditoss():
    
    temp_creditos = 0 # tempo que os creditos duram seram alterados durante os frames no caso [...]
    run_creditos_tutoriais = True
    
    while run_creditos_tutoriais == True:
        relogio.tick(4)
        tela.blit(fundo, (0, 0))

        Creditos = fonte_hud.render(("Jogo Feito Por:"), True, ('yellow'))

        lila = fonte.render(("Lila Maria Salvador Frazão"), True, ('yellow'))
        paulo = fonte.render(("Paulo Victor Alves Fabrício"), True, ('yellow'))
        pedro = fonte.render(("Pedro de Carvalho Chaaban"), True, ('yellow'))
        rian = fonte.render(("Rian Rodrigues Mourão"), True, ('yellow'))

        tela.blit(Creditos, (180, 70))

        tela.blit(lila, (230, 300))
        tela.blit(paulo, (230, 340))
        tela.blit(pedro, (230, 380))
        tela.blit(rian, (230, 420))
        temp_creditos += 1
        if temp_creditos > 4 * 5: # [...] para 5 segundos.
            run_creditos_tutoriais = False

        pygame.display.update()

# função de tutorial básico do game
def Tutoriaiss():
    # Inicializará o contador de tempo para o tutorial ficar na tela.
    temp_tutoriais = 0
    run_creditos_tutoriais = True
    while run_creditos_tutoriais == True:
        relogio.tick(4)
        tela.blit(fundo, (0, 0))
        # Título do tutorial
        Titulo = fonte_hud.render(("Tutorial:"), True, (255, 255, 255))
        # Textos
        Tutorial1 = fonte.render(("Jogin d'navyie é um Space atirarer inspirado no clássico dos vídeo games"),
                                    True, (217, 223, 225))
        Tutorial2 = fonte.render(("Space Invaders. Segue a lista de comandos do jogo:"), True, (217, 223, 225))
        # Instruções
        ImgTutorial = pygame.image.load("Tutorial.png")

        #Outline Título Tutorial
        Outline = fonte_hud.render(("Tutorial:"), True, (134, 151, 157))
        tela.blit(Outline, (303, 47)) # Superior Direito
        tela.blit(Outline, (303, 53)) # Superior Esquerdo
        tela.blit(Outline, (297, 47)) # Inferior Direito
        tela.blit(Outline, (297, 53)) # Inferior Esquerdo

        # Mostrar os textos e a imagem na tela
        tela.blit(Titulo, (300, 50))
        tela.blit(Tutorial1, (20, 150))
        tela.blit(Tutorial2, (20, 180))

        tela.blit(ImgTutorial, (0, 0))

        # Acrescenta ao contador, depois disso irá tirar a tela de tutorial.
        temp_tutoriais += 1
        if temp_tutoriais > 4 * 5:
            run_creditos_tutoriais = False

        pygame.display.update()

# tela final de cadastro do player
def gameover():
    reg = open('escore.txt', 'a') # arquivo que ficará guardado os scores, por enquanto não utilizáveis

    ramificação = fonte.render((over), True,('white'))  # escolha da mensagem de referência final do código


    #fontes utilizadas
    font = pygame.font.Font(None, 32) 
    terminator = pygame.font.Font(None, 46)


    #texto que mostra a pontuação final
    score = terminator.render((f'VOCÊ DEFENDEU SEU PLANETA DE {controle} HORDAS!'),True,(220,20,60))

    #seta o mouse para aparecer
    pygame.mouse.set_visible(True)

    #dimenções das 3 caixas de escrita que mudaram dependendo do jeito que forem feitas
    caixa_de_texto = pygame.Rect(largura/2-100, altura/2, 140, 32)
    caixa_inativa = pygame.Color('lightskyblue3')
    caixa_ativa = pygame.Color('dodgerblue2')


    # variaveis iniciais para serem modificadas pelo loop
    color = caixa_inativa
    ativo = False
    text = ''
    feito = True

    while feito:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # se tentar fechar a tela, apenas ira voltar para o loop inicial
                feito = False
            if event.type == pygame.MOUSEBUTTONDOWN: # evento que pega o clique do mouse no retangulo de digitação
                if caixa_de_texto.collidepoint(event.pos): 
                    ativo = not ativo# ativa e desativa a interação do retângulo
                else:
                    ativo = False
                color = caixa_ativa if ativo else caixa_inativa


            if event.type == pygame.KEYDOWN: # escritora da caixa de texto
                if ativo: # se tiver a caixa ativa:
                    if event.key == pygame.K_RETURN: # enter ira terminar o laço e setar o NickName
                        finalizadora = text
                        reg.write(f'{finalizadora} chegou na horda:{controle} \n')
                        feito = True

                    elif event.key == pygame.K_BACKSPACE: # é claro backspace deleta o ultimo elemento da string
                        text = text[:-1]

                    elif event.key == K_SPACE: # para fins de simplifação, espaço não funciona para o nickname
                        pass
                    elif len(text) == 5: #limite de 5 caracteres
                        pass
                    else:
                        text += event.unicode # e evento global que deixa termos do unicode.(permite acentos e etc etc.)



        # desenhos da tela | o que mostra na interface pro usuário
        tela.fill((20, 20, 30)) # cor do fundo

        # argumentos de escrita
        tuto = fonte.render('Clique na Caixa e Escreva seu Nickname (até 5 caracteres)', True, 'yellow')#tutorial inicial
        txto = font.render(text, True, color)# interface que mostra o que está sendo escrito
        width = 200 # largura da caixa de texto/ retangulos todos num geral.
        caixa_de_texto.w = width
        
        # o desenho dos argumentos
        tela.blit(score,(80,80))
        tela.blit(tuto, (115, altura-50))
        tela.blit(txto, (caixa_de_texto.x + 5, caixa_de_texto.y + 5))
        tela.blit(ramificação,(230, 250))
        pygame.draw.rect(tela, color, caixa_de_texto, 2)

        pygame.display.flip() # a atualização da tela usando flip.


# função do jogo principal utilizando a maioria das funções de interação

def jogo():

    #globais utilizadas na função
    global xdojogador
    global ydojogador
    global gatilho
    global kills
    
   #resets e presets
    count = 0
    municao = [] #lista de balas na tela 
    horda = [] # lista de inimigos na horda
    temp_gameover = 0

    pygame.mouse.set_visible(False) # tira o mouse da tela

    Run = True
    while Run:  # definindo o loop
        # desenhando primeiro na primeira camada, o fundo do game
        tela.blit(fundo, (0, 0))
        # pontuação atual/contagem da horda
        pon =  f'Horda atual: {controle}'
        # Criando a mensagem que será escrita na tela
        mensagem = f"Vidas: {pontos}"

        #variavel que sera desenhada
        hrd = fonte.render(pon, True, (200, 200, 200))
        texto = fonte.render(mensagem, True, (200, 200, 200))

        # Criando o que será exibido na tela, a partir das variáveis fonte(a qual definiu como será escrito de escrito o texto) e a mensagem( que é oq será escrito de fato. os parâmetros recebidos por esse comando é: 1: texto, 2:Não pixelalização, 3: cor)
        game_over = pygame.transform.scale(pygame.image.load("GameOver.png"),(500,150))
        # Função tick parte intregante de clock que onde se define os frames por segundo
        relogio.tick(30)
        # Dentro do código principal em loop há de ser necessário outro loop capaz de verificar a atualização dos comandos indicados pelo o usuário. Para isso ele cria condições para eventos.
        for event in pygame.event.get():
            # saída do jogo
            if (event.type == QUIT):
                pygame.quit()
                # importanto função da biblioteca sys
                exit()

            # Caso queira fazer um movimentação em que uma tecla apertada n tenha resposta no jogo:

            if (event.type) == KEYDOWN: # Evento do tipo KEYDOWN, que possibilita o uso de teclas.
                # Caso aperte ESC, o laço é interrompido, fazendo assim o jogo parar.
                if (event.key == K_ESCAPE):
                    Run = False
            # Caso queira uma movimentação continua com resposta a tecla apertada usas-se get_pressed:
            # Definindo a a tecla 'a' como tecla de movimentação para a esquerda.
            if (pygame.key.get_pressed()[K_a]):
                # Calculo feito a partir de como é distribuido os pontos de x na tela.
                if xdojogador <= 0:
                    pass
                else:
                    xdojogador -= 15
            # Definindo a a tecla 'd' como tecla de movimentação para a direita.
            if (pygame.key.get_pressed()[K_d]):
                # Calculo feito a partir de como é distribuido os pontos de x na tela.
                if xdojogador >= largura - 64:
                    pass
                else:
                    xdojogador += 15

            # Atirar com o w
            if count <= 0: # temporizador para não haver spam de balas
                # Definindo a a tecla 'w' como tecla de comando para atirar.
                if pygame.key.get_pressed()[K_w] and pontos != 0:
                    gatilho = True
                # sendo 30 quadros, é possível atirar até 5 balas por segundo
                count = 6

        if count > 0: # bala vai diminuir 1 por frame
            count -= 1

        municao = atirar(municao) # retornando o valor atual da lista de munições

        horda = SpawnInimigos(horda) # retornando o valor atual da lista de inimigos na horda

        #Chamada da função colisão para cada inimigo da horda.
        """Se de algum dos projéteis desparado pelo player atingir(chamada da função colisão) algum dos inimigos da da horda,
           o inimigo é deletado da horda e o projétil movido para onde ele é deletado, no caso o topo da tela """

        for inimigo in horda: 
            
            for balas in municao:
                if colisao(inimigo.x, inimigo.y, balas.x, balas.y) == True:
                    balas.y = -20

                    del horda[horda.index(inimigo)]
                    kills += 1

        # verificação e movimentação do player pela função que desenha o sprite do player
        xdojogador += atua_xdoj
        # Chamando a função para desenhar o personagem aliado.
        jogador(xdojogador,ydojogador) 

        # se as vidas zeram, é desenhado o game over e, logo depois um certo tempo, começa a tela de game over antes de fechar o game
        if pontos <= 0:
            tela.blit(game_over, (200, 240))
            temp_gameover += 1
            if temp_gameover > 30 * 2:
                gameover()
                Run = False
        # comando que expõem de fato um texto na tela, o 1 parâmetro recebido é oque será escrito e as suas configurações e o 2 é onde.
        tela.blit(texto, (largura-120,50))
        tela.blit(hrd,(largura-180,100))
        # a tela do jogo está sendo atualizada a cada loop do jogo, ou seja, a cada verificação de evento.
        pygame.display.update()

# O main loop para a atualização em tempo real do jogo.
while True:
    relogio.tick(10)
    tela.fill((0, 0, 0))

    over = choice(referencias)

    initial  = pygame.Rect(xi, yi, 20, 60)
    play     = pygame.Rect(300, 260, 250, 60)
    creditos = pygame.Rect(300, 340, 250, 60)
    Tutorial = pygame.Rect(300, 420, 250, 60)

    nomeJogo = (pygame.image.load("TituloJogo.png"))

    tela.blit(nomeJogo, (60, 50))

    msg_menu_cmd = fonte.render(('  W | S para ir pra cima e para baixo                     Espaço para selecionar'), True,'yellow')

    msg_menu_play = fonte_menu.render(("Jogar"), True, (255, 255, 255))
    msg_menu_tutoriais = fonte_menu.render(("Tutoriais"), True, (255, 255, 255))
    msg_menu_creditos = fonte_menu.render(("Créditos"), True, (255, 255, 255))

    # uma pequena interação gráfica, que faz o quadrado inicial ficar piscado
    if intera == 0:   
        pygame.draw.rect(tela, (255, 255, 255), initial)
        intera = 3

    intera -= 1

    # desenho dos botões de seleção
    pygame.draw.rect(tela, 'dodgerblue1', play)
    tela.blit(msg_menu_play, (play))
    pygame.draw.rect(tela, 'orange', creditos)
    tela.blit(msg_menu_creditos, (creditos))
    pygame.draw.rect(tela, 'red', Tutorial)
    tela.blit(msg_menu_tutoriais, (Tutorial))
    tela.blit(msg_menu_cmd,(10,altura-40))

    # dentro do código principal em loop há de ser necessário outro loop capaz de verificar a atualização dos comandos indicados pelo o usuário. Para isso a posição do retangulo cria condições para eventos.
    for event in pygame.event.get():
        if (event.type == QUIT):  # saída do jogo
            pygame.quit()
            exit()
        if (event.type == KEYDOWN):
            if event.key == K_w and initial.y != play.y:
                yi -= 80

            if event.key == K_s and initial.y != Tutorial.y:
                yi += 80

            if event.key == K_SPACE and initial.y == creditos.y:
                creditoss()

            if event.key == K_SPACE and initial.y == play.y:
                #altera
                pontos = 10
                kills = 0
                maximo = 0
                controle = 0
                jogo()
                

            if event.key == K_SPACE and initial.y == Tutorial.y:
                Tutoriaiss()
                
                

    pygame.display.update()