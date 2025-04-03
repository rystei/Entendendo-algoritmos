import pygame
import time
import heapq

# Definição de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)

# Configuração da tela do Pygame
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador do 8-Puzzle - A* com heurística")

# Estado inicial e objetivo
estado_inicial = [[8, 2, 5], [4, 0, 6], [7, 3, 1]]
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

def gerar_vizinhos(estado):
    vizinhos = []
    for direcao in movimentos:
        novo_estado = mover(estado, direcao)
        if novo_estado:
            vizinhos.append(novo_estado)
    return vizinhos

def estados_iguais(e1, e2):
    return all(e1[i][j] == e2[i][j] for i in range(3) for j in range(3))

def serializar(estado):
    return tuple(tuple(linha) for linha in estado)

def pecas_corretas(estado, objetivo):
    return sum(
        1 for i in range(3) for j in range(3)
        if estado[i][j] != 0 and estado[i][j] == objetivo[i][j]
    )

def pecas_fora_do_lugar(estado, objetivo):
    return sum(
        1 for i in range(3) for j in range(3)
        if estado[i][j] != 0 and estado[i][j] != objetivo[i][j]
    )

def distancia_manhattan(estado, objetivo):
    posicoes_objetivo = {objetivo[i][j]: (i, j) for i in range(3) for j in range(3)}
    distancia = 0
    for i in range(3):
        for j in range(3):
            valor = estado[i][j]
            if valor != 0:
                oi, oj = posicoes_objetivo[valor]
                distancia += abs(i - oi) + abs(j - oj)
    return distancia

def a_estrela(inicio, objetivo, heuristica):
    memoria = {
        'visitados': 0,
        'estados_unicos': set(),
        'max_profundidade': 0
    }
    
    visitados = set()
    fila = []
    heapq.heappush(fila, (heuristica(inicio, objetivo), 0, inicio, []))
    
    while fila:
        estimativa_total, custo, estado_atual, caminho = heapq.heappop(fila)
        estado_serial = serializar(estado_atual)
        memoria['visitados'] += 1
        
        if estado_serial in visitados:
            continue
            
        visitados.add(estado_serial)
        memoria['estados_unicos'].add(estado_serial)
        memoria['max_profundidade'] = max(memoria['max_profundidade'], len(caminho))
        
        if estados_iguais(estado_atual, objetivo):
            return caminho + [estado_atual], memoria
        
        for vizinho in gerar_vizinhos(estado_atual):
            if serializar(vizinho) not in visitados:
                novo_caminho = caminho + [estado_atual]
                novo_custo = custo + 1
                prioridade = novo_custo + heuristica(vizinho, objetivo)
                heapq.heappush(fila, (prioridade, novo_custo, vizinho, novo_caminho))
    
    return None, memoria

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

def exibir_estatisticas(caminho, objetivo, memoria):
    if not caminho:
        return

    print("\nEstatísticas detalhadas:")
    print(f"Total de estados visitados: {memoria['visitados']}")
    print(f"Estados únicos na memória: {len(memoria['estados_unicos'])}")
    print(f"Profundidade máxima alcançada: {memoria['max_profundidade']}")
    print(f"Comprimento da solução: {len(caminho)-1} movimentos\n")

    print("Progresso por estado:")
    for idx, estado in enumerate(caminho):
        corretas = pecas_corretas(estado, objetivo)
        manhattan = distancia_manhattan(estado, objetivo)
        print(f"Estado {idx}:")
        print(f"Peças no lugar: {corretas}/8")
        print(f"Distância Movimento total: {manhattan}")
        if idx > 0:
            diff = [(i,j) for i in range(3) for j in range(3) 
                   if caminho[idx-1][i][j] != estado[i][j]]
            print(f"Peça movida: {estado[diff[0][0]][diff[0][1]]}")
        print("-------------------")

# Execução principal
caminho_solucao, memoria = a_estrela(estado_inicial, estado_objetivo, distancia_manhattan)

if caminho_solucao:
    executar_simulacao(caminho_solucao)
    exibir_estatisticas(caminho_solucao, estado_objetivo, memoria)
else:
    print("Nenhuma solução encontrada.")