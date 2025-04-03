import pygame
import time
from collections import deque

# Definição de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)

# Configuração da tela do Pygame
WIDTH, HEIGHT = 400, 400
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador do 8-Puzzle - DFS")

# Estado inicial e objetivo
estado_inicial = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
estado_objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Movimentos possíveis
movimentos = {
    "↑": (-1, 0),
    "↓": (1, 0),
    "←": (0, -1),
    "→": (0, 1)
}

# Função para encontrar a posição do zero (espaço vazio)
def encontrar_zero(estado):
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                return i, j

# Função para mover o zero
def mover(estado, direcao):
    i, j = encontrar_zero(estado)
    di, dj = movimentos[direcao]
    novo_i, novo_j = i + di, j + dj

    if 0 <= novo_i < 3 and 0 <= novo_j < 3:
        novo_estado = [linha[:] for linha in estado]  # Copia o tabuleiro
        novo_estado[i][j], novo_estado[novo_i][novo_j] = novo_estado[novo_i][novo_j], novo_estado[i][j]
        return novo_estado

    return None  # Movimento inválido

# Implementação da Busca em Profundidade (DFS)
def dfs(inicio, objetivo):
    stack = [(inicio, [])]  # Pilha de estados e seus caminhos
    visitados = set()

    while stack:
        estado, caminho = stack.pop()
        estado_tuple = tuple(map(tuple, estado))  # Converte para tupla para poder adicionar no set

        if estado_tuple in visitados:
            continue

        visitados.add(estado_tuple)

        if estado == objetivo:
            return caminho + [estado]

        for direcao in movimentos:
            novo_estado = mover(estado, direcao)
            if novo_estado:
                stack.append((novo_estado, caminho + [estado]))

    return None  # Nenhuma solução encontrada

# Função para desenhar o tabuleiro do 8-Puzzle no Pygame
def desenhar_tabuleiro(estado):
    screen.fill(WHITE)
    tam_celula = WIDTH // 3

    for i in range(3):
        for j in range(3):
            num = estado[i][j]
            rect = pygame.Rect(j * tam_celula, i * tam_celula, tam_celula, tam_celula)
            pygame.draw.rect(screen, BLUE if num == 0 else GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 3)

            if num != 0:
                font = pygame.font.Font(None, 60)
                text = font.render(str(num), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    pygame.display.flip()

# Loop de animação da solução
def executar_simulacao(caminho):
    clock = pygame.time.Clock()

    for estado in caminho:
        desenhar_tabuleiro(estado)
        time.sleep(1)
        clock.tick(1)

    time.sleep(2)
    pygame.quit()

# Obtém o caminho da solução usando DFS
caminho_solucao = dfs(estado_inicial, estado_objetivo)

if caminho_solucao:
    executar_simulacao(caminho_solucao)
else:
    print("Nenhuma solução encontrada")