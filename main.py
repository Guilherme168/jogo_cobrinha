#baixar e importar a biblioteca pygame
import pygame
from pygame.locals import *   #importar essa sub lib para poder utilizar a função pygame.event.get()
import random
import time

pygame.font.init()   #iniciar as fontes pelo pygame
font = pygame.font.SysFont('Arial', 35, True, True)  #escolher a fonte através das fontes do sistema + seu tamanho e se é negrito e italico
# pygame.font.get_fonts()  mostra todas as fontes disponiveis


#definir as dimensões da janela onde o jogo irá ser reproduzido
#Através de constantes que receberão suas dimensões
WINDOW_HEIGHT = 600   #constantes devem ser definidas sempre com letra maiuscula no python. Boas práticas
WINDOW_WIDTH = 600

BLOCK = 10  #dimensão da cobra
INITIAL_POSITION_X = WINDOW_WIDTH / 2  #indica a posição inicial da cobra no eixo x
INITIAL_POSITION_Y = WINDOW_HEIGHT / 2  #indica a posição inicial da cobra no eixo y

#criar a superficie onde a cobra deslizará
snake_surface = pygame.Surface((BLOCK, BLOCK))  #dimensões da cobra, 10 x 10
snake_surface.fill((53, 59, 72))  #mudar a cor da cobra
snake_position = [(INITIAL_POSITION_X, INITIAL_POSITION_Y), (INITIAL_POSITION_X + BLOCK, INITIAL_POSITION_Y), (INITIAL_POSITION_X + 2 * BLOCK, INITIAL_POSITION_Y)]  #instruções de onde a cobra aparecerá inicialmente e suas subsequentes posições
direcao = K_LEFT   #seu valor inicial aponta para à seta esquerda
speed = 10  #velocidade inicial da cobra
points = 0 #variavel para guardar os pontos


#criar obstaculos
obstacle_surface = pygame.Surface((BLOCK, BLOCK))
obstacle_surface.fill((0, 0, 0))
obstacle_position = []  #ficará vázio pois não deverá aparecer no começo, apenas quando houver colisão com maças

pygame.display.set_caption('Jogo da Cobrinha')

def generate_position():   #função para gerar, aleatoriamente, as coordenadas da posição da maça
    x = random.randint(0, WINDOW_WIDTH)
    y = random.randint(0, WINDOW_HEIGHT)
    if (x,y) in obstacle_position:   #impedir que algum obstaculo seja gerado em cima de uma maça ou dois obstaculos um em cima do outro
        generate_position()
    return x // BLOCK * BLOCK, y // BLOCK * BLOCK   #ajuste para fazer com que as coordenadas geradas estejam sempre de acordo com o passo da cobra (10x10)


def collision (pos1, pos2):  #função que vai  retornar a igualdade entre as posições da maça e cobra
    return pos1 == pos2


#criar as maças
apple_surface = pygame.Surface((BLOCK, BLOCK))  #dimensões da maça 10x10
apple_position = generate_position()  #posição da maça gerada aleatoriamente
apple_surface.fill((255, 0, 0))  #cor vermelha para a maça

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  #as dimensões devem ser passadas em tupla



def verify_margin (pos):  #função para verificar a posição da cobra em relação às margens
    if 0 <= pos[0] < WINDOW_WIDTH and 0 <= pos[1] < WINDOW_HEIGHT:
        return False
    else:
        return True

def game_over (): #função para game over
    font_game_over = pygame.font.SysFont('Arial', 60, True, True)  #escolher a fonte através das fontes do sistema + seu tamanho e se é negrito e italico
    text_game_over = 'Game Over'
    over = font_game_over.render(text_game_over, True, (255,255,255))
    window.blit(over, (140, 300))
    pygame.display.update()
    time.sleep(5)
    pygame.quit()  #fechar o jogo
    quit()  #fechar a janela


while True:
    pygame.time.Clock().tick(speed)  #dita a velocidade com que a cobra irá se mover
    window.fill((68, 189, 50))  #prencher a cor da janela com alguma cor através de coordenadas RGB

    message = f'Pontos: {points}'   #mensagem que será formatada
    text = font.render(message, True, (255,255,255))  #(RGB sempre ser passado em tupla)

    for evento in pygame.event.get():  #iterar cada evento que ocorrer durante a execução para 'armazená-lo'
        if evento.type == QUIT:    #condição para fechar o jogo
            pygame.quit()  #fechar o jogo
            quit()  #fechar a janela

        elif evento.type == KEYDOWN:   #condição para identificar evento de tecla
            if evento.key in (K_RIGHT, K_LEFT, K_DOWN, K_UP):  #condição para identficar o tipo de evento de tecla
                if evento.key == K_DOWN and direcao == K_UP:
                    continue
                elif evento.key == K_UP and direcao == K_DOWN:
                    continue
                elif evento.key == K_RIGHT and direcao == K_LEFT:   #condições para impedir colisão com o corpo ao mudar a direção em 180°. Continue vai fazer com que o loop continue e a direção não será atualizada
                    continue
                elif evento.key == K_LEFT and direcao == K_RIGHT:
                    continue
                direcao = evento.key   #variavel que vai indicar a direção em que a cobra vai se movimentar. Sempre irá mudar quando um evento de tecla for captado.


    window.blit(apple_surface, apple_position)  #renderizar a maça

    if collision(snake_position[0], apple_position):   #condicao que, se verdadeiro o que há na função, irá retornar uma nova posição aleatória para a maça
        snake_position.append((-10, -10))  # aumentar o tamanho da cobra adicionando mais pixels ao final da lista de sua posição
        apple_position = generate_position()
        obstacle_position.append(generate_position())  #gerar um novo obstaculo após uma colisão com maça
        points += 1  #somar um ponto sempre que comer uma maça
        if points % 5 == 0:  #a cada 5 maças comidas, aumentar a velocidade da cobra
            speed += 2


    for pos in snake_position:
        window.blit(snake_surface, pos)   #para cada posição na lista de posições, renderizar a cobra corretamente

    for item in range(len(snake_position) -1, 0, -1):
        if collision(snake_position[0], snake_position[item]):  #caso a cabeça da cobra ([0]) colida com o corpo ([item]), é fim de jogo
            game_over()
        snake_position[item] = snake_position[item-1]

    for pos in obstacle_position:
        window.blit(obstacle_surface, pos)
        if collision(snake_position[0], pos):  #passará por todas as posições dos obstaculos e, se a cabeça da cobra colidir com algum, o jogo acaba
           game_over()

    if verify_margin(snake_position[0]):  #se a cabeça da cobra cruzar os limites da tela, o jogo acaba.
        game_over()

    #formatar o movimento em relação o eixo x (horizontalmente)
    if direcao == K_RIGHT:
     snake_position[0] = snake_position[0][0] + BLOCK, snake_position[0][1]  #mover a cobra para a direita
    elif direcao == K_LEFT:
     snake_position[0] = snake_position[0][0] - BLOCK, snake_position[0][1]  #mover a cobra para a esquerda

    #formatar o movimento em relação o eixo y (verticalmente)
    elif direcao == K_DOWN:
     snake_position[0] = snake_position[0][0], snake_position[0][1] + BLOCK  #mover a cobra para baixo
    elif direcao == K_UP:
     snake_position[0] = snake_position[0][0], snake_position[0][1] - BLOCK  #mover a cobra para a cima

    window.blit(text, (420, 30))  #formatar o texto no jogo, passando o mesmo + suas coordenadas x e y
    pygame.display.update()  #atualizar a tela sempre que houver qualquer modificação