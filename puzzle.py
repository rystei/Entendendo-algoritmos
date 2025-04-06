import pygame
import time
import heapq
from collections import deque

# Definição de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)

# Configuração da tela do Pygame
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador do 8-Puzzle")

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

def encontrar_zero(estado):
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                return i, j

def mover(estado, direcao):
    i, j = encontrar_zero(estado)
    di, dj = movimentos[direcao]
    novo_i, novo_j = i + di, j + dj

    if 0 <= novo_i < 3 and 0 <= novo_j < 3:
        novo_estado = [linha[:] for linha in estado]
        novo_estado[i][j], novo_estado[novo_i][novo_j] = novo_estado[novo_i][novo_j], novo_estado[i][j]
        return novo_estado
    return None

def bfs(inicio, objetivo):
    fila = deque([(inicio, [])])
    visitados = set()
    
    while fila:
        estado, caminho = fila.popleft()
        estado_tuple = tuple(tuple(linha) for linha in estado)
        
        if estado_tuple in visitados:
            continue
        visitados.add(estado_tuple)
        
        if estado == objetivo:
            return caminho + [estado]
        
        for direcao in movimentos:
            novo_estado = mover(estado, direcao)
            if novo_estado:
                fila.append((novo_estado, caminho + [estado]))
    
    return None

def dfs(inicio, objetivo):
    pilha = [(inicio, [])]
    visitados = set()
    
    while pilha:
        estado, caminho = pilha.pop()
        estado_tuple = tuple(tuple(linha) for linha in estado)
        
        if estado_tuple in visitados:
            continue
        visitados.add(estado_tuple)
        
        if estado == objetivo:
            return caminho + [estado]
        
        for direcao in movimentos:
            novo_estado = mover(estado, direcao)
            if novo_estado:
                pilha.append((novo_estado, caminho + [estado]))
    
    return None

def heuristica_pecas(inicio, objetivo):
    fila = []
    heapq.heappush(fila, (0, inicio, [], {'visitados': 0, 'pecas_corretas': []}))
    visitados = set()
    
    while fila:
        _, estado, caminho, historico = heapq.heappop(fila)
        estado_tuple = tuple(tuple(linha) for linha in estado)
        
        if estado_tuple in visitados:
            continue
        visitados.add(estado_tuple)
        
        pecas_corretas = sum(1 for i in range(3) for j in range(3) 
                           if estado[i][j] != 0 and estado[i][j] == objetivo[i][j])
        historico['pecas_corretas'].append(pecas_corretas)
        historico['visitados'] += 1
        
        if estado == objetivo:
            print("\nHistórico de peças corretas durante a busca:")
            print(f"Quantidade em cada passo: {historico['pecas_corretas']}")
            print(f"Total de estados visitados: {historico['visitados']}")
            return caminho + [estado]
        
        for direcao in movimentos:
            novo_estado = mover(estado, direcao)
            if novo_estado:
                novo_caminho = caminho + [estado]
                pecas_fora = sum(1 for i in range(3) for j in range(3) 
                               if novo_estado[i][j] != 0 and novo_estado[i][j] != objetivo[i][j])
                heapq.heappush(fila, (pecas_fora, novo_estado, novo_caminho, historico))
    
    return None

def heuristica_movimentos(inicio, objetivo):
    fila = []
    heapq.heappush(fila, (0, inicio, [], {'visitados': 0, 'distancias': []}))
    visitados = set()
    
    while fila:
        _, estado, caminho, historico = heapq.heappop(fila)
        estado_tuple = tuple(tuple(linha) for linha in estado)
        
        if estado_tuple in visitados:
            continue
        visitados.add(estado_tuple)
        
        distancia_total = 0
        for i in range(3):
            for j in range(3):
                if estado[i][j] != 0:
                    for x in range(3):
                        for y in range(3):
                            if objetivo[x][y] == estado[i][j]:
                                distancia_total += abs(i - x) + abs(j - y)
                                break
        historico['distancias'].append(distancia_total)
        historico['visitados'] += 1
        
        if estado == objetivo:
            print("\nHistórico de distâncias durante a busca:")
            print(f"Distância em cada passo: {historico['distancias']}")
            print(f"Total de estados visitados: {historico['visitados']}")
            return caminho + [estado]
        
        for direcao in movimentos:
            novo_estado = mover(estado, direcao)
            if novo_estado:
                novo_caminho = caminho + [estado]
                nova_distancia = 0
                for i in range(3):
                    for j in range(3):
                        if novo_estado[i][j] != 0:
                            for x in range(3):
                                for y in range(3):
                                    if objetivo[x][y] == novo_estado[i][j]:
                                        nova_distancia += abs(i - x) + abs(j - y)
                                        break
                heapq.heappush(fila, (nova_distancia, novo_estado, novo_caminho, historico))
    
    return None

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

def executar_simulacao(caminho):
    pygame.init()
    clock = pygame.time.Clock()

    for estado in caminho:
        desenhar_tabuleiro(estado)
        time.sleep(0.5)
        clock.tick(1)
        pygame.event.pump()

    time.sleep(1)
    pygame.quit()

caminho_solucao = heuristica_movimentos(estado_inicial, estado_objetivo)
caminho_solucao = bfs(estado_inicial, estado_objetivo)


if caminho_solucao:
    print(f"\nSolução encontrada em {len(caminho_solucao)-1} movimentos!")
    executar_simulacao(caminho_solucao)
else:
    print("Nenhuma solução encontrada.")
