# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search
import sys
import argparse
import numpy as np

class RRState:
    statde_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1
    
    def __lt__(self, other):
        return self.id < other.id

class Board:
    def __init__(self, N: int):
        self.size = N
        self.board = [[ 0 for i in range(self.size)] for j in range(self.size)]
        self.internal_walls = [[ 0 for i in range(self.size)] for j in range(self.size)]
 
    def printBoard(self):
        print(self.board)
        print(self.internal_walls)

    def addRobot(self, color: str, x: int, y: int):
        self.board[x - 1][y - 1] = color
    
    def addTarget(self, color: str, x: int, y: int):
        self.board[x - 1][y - 1] = "t" + color

    def addNumberWalls(self, n: int):
        self.n_walls = n
    
    def addInternalWalls(self, x: int, y: int, pos: str):
        self.internal_walls[x - 1][y - 1] = pos

    def robot_position(self, robot: str):
        a = np.array(self.board)
        result = np.where(a == robot)
        coor = list(zip(result[0] + 1, result[1] + 1))
        return coor[0]
        pass
    
    # TODO: outros metodos da classe

def parse_instance(filename: str) -> Board:
    # TODO
    f = open(filename, 'r')
    board = Board(int(f.readline()))
    for i in range(4):
        array = (f.readline()).split()
        board.addRobot(array[0], int(array[1]), int(array[2]))
    array = (f.readline()).split()
    board.addTarget(array[0], int(array[1]), int(array[2]))
    n_walls = f.readline()
    board.addNumberWalls(int(n_walls))
    for i in range(int(n_walls)):
        array = (f.readline()).split()
        board.addInternalWalls(int(array[0]), int(array[1]), array[2])
    return board
    pass

class RicochetRobots(Problem):
    #input_seq[[ix1, ix2]] = input_seq[[ix2, ix1]]

    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        # TODO: self.initial = ...
        pass

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # TODO
        pass

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        # TODO
        pass

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    parse_instance(sys.argv[1])
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass