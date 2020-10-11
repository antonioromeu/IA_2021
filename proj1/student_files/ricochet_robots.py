# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 92509 Leonor Veloso
# 92427 António Romeu Pinheiro

from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search
import sys
import argparse
import numpy as np

class RRState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1
    
    def __lt__(self, other):
        return self.id < other.id

class Board:
    def __init__(self, N: int):
        self.size = N
        self.board = [[ '0' for i in range(self.size)] for j in range(self.size)]
        self.internal_walls = [[ () for i in range(self.size)] for j in range(self.size)]
 
    def printBoard(self):
        print(self.board)

    def addRobot(self, color: str, x: int, y: int):
        self.board[x - 1][y - 1] = color
    
    def addTarget(self, color: str, x: int, y: int):
        self.board[x - 1][y - 1] = "t" + color

    def addNumberWalls(self, n: int):
        self.n_walls = n
    
    def addInternalWalls(self, l: int, c: int, pos: str):
        if pos == 'r':
            self.internal_walls[l - 1][c - 1] += (pos, )
            self.internal_walls[l - 1][c] += ('l', )
        elif pos == 'l':
            self.internal_walls[l - 1][c - 1] += (pos, )
            self.internal_walls[l - 1][c - 2] += ('r', )
        elif pos == 'd':
            self.internal_walls[l - 1][c - 1] += (pos, )
            self.internal_walls[l][c - 1] += ('u', )
        elif pos == 'u':
            self.internal_walls[l - 1][c - 1] += (pos, )
            self.internal_walls[l - 2][c - 1] += ('d', )

    def existsWall(self, coor: tuple, dir: str):
        print(dir in self.internal_walls[coor[0] - 1][coor[1] - 1])
        return dir in self.internal_walls[coor[0] - 1][coor[1] - 1]

    def swapPos(self, robot: tuple, dir: str):
        new_pos = (-1, -1)
        print("no swap pos " + dir)
        print(robot)
        if self.existsWall(robot, dir):
            return new_pos
        if dir == 'u' and robot[0] - 1 != 0 and self.board[robot[0] - 2][robot[1] - 1] == '0':
            self.board[robot[0] - 1][robot[1]] = self.board[robot[0]][robot[1]]
            self.board[robot[0]][robot[1]] = '0'
            new_pos = (robot[0] - 1, robot[1])
        elif dir == 'd' and robot[0] - 1 != 3 and self.board[robot[0]][robot[1] - 1] == '0':
            print("down")
            self.board[robot[0]][robot[1] - 1] = self.board[robot[0]][robot[1]]
            self.board[robot[0]][robot[1]] = '0'
            new_pos = (robot[0] + 1, robot[1])
        elif dir == 'r' and robot[1] - 1 != 3 and self.board[robot[0] - 1][robot[1]] == '0':
            print("right")
            self.board[robot[0]][robot[1] + 1] = self.board[robot[0]][robot[1]]
            self.board[robot[0]][robot[1]] = '0'
            new_pos = (robot[0], robot[1] + 1)
        elif dir == 'l' and robot[1] - 1 != 0 and self.board[robot[0] - 1][robot[1] - 2] == '0':
            print("left")
            self.board[robot[0]][robot[1] - 1] = self.board[robot[0]][robot[1]]
            self.board[robot[0]][robot[1]] = '0'
            new_pos = (robot[0], robot[1] - 1)
        return new_pos

    def slideAway(self, robot: tuple, dir: str):
        aux = self.swapPos(robot, dir)
        if aux == (-1, -1):
            return
        else:
            self.slideAway(aux, dir)

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
    #board.printBoard()
    return board
    pass

class RicochetRobots(Problem):

    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = board
        pass

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        board = state.board
        self.actions = []
        for robot in ['R', 'G', 'B', 'Y']:
            pos = board.robot_position(robot)
            for dir in ['u', 'd', 'l', 'r']:
                if board.swapPos((pos[0] - 1, pos[1] - 1), dir) != (-1, -1):
                    if dir == 'u':
                        board.swapPos((pos[0] - 2, pos[1] - 1), 'd')
                    elif dir == 'd':
                        board.swapPos((pos[0], pos[1] - 1), 'u')
                    elif dir == 'l':
                        board.swapPos((pos[0] - 1, pos[1] - 2), 'r')
                    elif dir == 'r':
                        board.swapPos((pos[0] - 1, pos[1]), 'l')
                    self.actions.append((robot, dir))
        print(self.actions)
        return self.actions
        pass

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """

        robot_pos = state.board.robot_position(action[0])
        print(robot_pos)
        print(action[1])
        state.board.printBoard()
        state.board.slideAway(robot_pos, action[1])
        state.board.printBoard()
        return state
        pass

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        # TODO
        pass

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        #manhattan distance:
        #function heuristic(node) =
            #dx = abs(node.x - goal.x)
            #dy = abs(node.y - goal.y)
            #return D * (dx + dy)
        # TODO
        pass

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    board = parse_instance(sys.argv[1])
    problem = RicochetRobots(board)
    problem.result(RRState(board), ('R', 'u'))
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass