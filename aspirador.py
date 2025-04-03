import pygame
import time
from collections import deque

# Definições de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (100, 255, 100)
RED = (255, 100, 100)

# Configuração da tela
WIDTH, HEIGHT = 400, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador do Mundo do Aspirador")

# Estados iniciais do ambiente
estado_inicial = ('L', 'S', 'S')  # (Posição, Estado da Sala L, Estado da Sala R)
objetivo = ('L', 'C', 'C')  # Objetivo (Ambas as salas limpas)

# Definição do espaço de estados
acoes = {
    "ESQ": lambda p, l, r: ('L', l, r) if p == 'R' else (p, l, r),
    "DIR": lambda p, l, r: ('R', l, r) if p == 'L' else (p, l, r),
    "ASP": lambda p, l, r: ('L', 'C', r) if p == 'L' else ('R', l, 'C')
}

# Busca em Largura (BFS) para encontrar o caminho ótimo
def bfs(inicio, objetivo):
    fila = deque([[inicio]])  # Começa com o estado inicial
    visitados = set()

    while fila:
        caminho = fila.popleft()
        estado_atual = caminho[-1]

        if estado_atual == objetivo:
            return caminho  # Caminho encontrado

        if estado_atual not in visitados:
            visitados.add(estado_atual)
            for acao, transicao in acoes.items():
                novo_estado = transicao(*estado_atual)
                novo_caminho = caminho + [novo_estado]
                fila.append(novo_caminho)

    return None  # Nenhum caminho encontrado

# Obtém o caminho da solução
caminho_solucao = bfs(estado_inicial, objetivo)

# Função para desenhar o ambiente
def desenhar_ambiente(estado):
    screen.fill(WHITE)

    # Definição das posições das salas
    sala_l = pygame.Rect(50, 50, 120, 100)
    sala_r = pygame.Rect(230, 50, 120, 100)

    # Definição da posição do aspirador
    pos, l, r = estado

    # Desenha as salas
    pygame.draw.rect(screen, GREEN if l == 'C' else RED, sala_l)
    pygame.draw.rect(screen, GREEN if r == 'C' else RED, sala_r)

    # Desenha os contornos das salas
    pygame.draw.rect(screen, BLACK, sala_l, 3)
    pygame.draw.rect(screen, BLACK, sala_r, 3)

    # Desenha o aspirador
    aspirador_x = 110 if pos == 'L' else 290
    pygame.draw.circle(screen, BLACK, (aspirador_x, 100), 20)

    # Exibe o estado atual
    font = pygame.font.Font(None, 24)
    texto = font.render(f"Estado: {estado}", True, BLACK)
    screen.blit(texto, (120, 10))

    pygame.display.flip()

# Loop de animação do aspirador
def executar_simulacao(caminho):
    pygame.init()
    clock = pygame.time.Clock()

    for estado in caminho:
        desenhar_ambiente(estado)
        time.sleep(2)  # Tempo entre os movimentos
        clock.tick(2)

    time.sleep(3)  # Aguarda antes de fechar
    pygame.quit()

# Executa a simulação
executar_simulacao(caminho_solucao)