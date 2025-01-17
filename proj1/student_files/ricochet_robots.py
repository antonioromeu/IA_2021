# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 59:
# 92509 Leonor Veloso
# 92427 António Romeu Pinheiro

from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, InstrumentedProblem
import sys
import argparse
import numpy as np
from math import sqrt
import time

class RRState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1
    
    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, state):
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] != state.board.board[i][j]:
                    return False
        return True
    
    def __hash__(self):
        return self.id % 7

class Board:
    def __init__(self, N: int):
        self.size = N
        self.board = [[ '0' for i in range(self.size)] for j in range(self.size)]
        self.internal_walls = [[ () for i in range(self.size)] for j in range(self.size)]
        self.robotOnTarget = False
        self.targetPos = (-1, -1)
        self.targetColor = "BLACKPINK"

    def addRobot(self, color: str, x: int, y: int):
        self.board[x - 1][y - 1] = color
    
    def addTarget(self, color: str, x: int, y: int):
        self.targetPos = (x - 1, y - 1)
        self.targetColor = color

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
        return dir in self.internal_walls[coor[0]][coor[1]]

    def swapPos(self, robot: tuple, dir: str):
        new_pos = (-1, -1)
        if self.existsWall(robot, dir):
            return new_pos
        if dir == 'u' and robot[0] != 0 and self.board[robot[0] - 1][robot[1]] == '0':
            self.board[robot[0] - 1][robot[1]] = self.board[robot[0]][robot[1]]
            self.board[robot[0]][robot[1]] = '0'
            new_pos = (robot[0] - 1, robot[1])
        elif dir == 'd' and robot[0] != self.size - 1 and self.board[robot[0] + 1][robot[1]] == '0':
            self.board[robot[0] + 1][robot[1]] = self.board[robot[0]][robot[1]]
            self.board[robot[0]][robot[1]] = '0'
            new_pos = (robot[0] + 1, robot[1])
        elif dir == 'r' and robot[1] != self.size - 1 and self.board[robot[0]][robot[1] + 1] == '0':
            self.board[robot[0]][robot[1] + 1] = self.board[robot[0]][robot[1]]
            self.board[robot[0]][robot[1]] = '0'
            new_pos = (robot[0], robot[1] + 1)
        elif dir == 'l' and robot[1] != 0 and self.board[robot[0]][robot[1] - 1] == '0':
            self.board[robot[0]][robot[1] - 1] = self.board[robot[0]][robot[1]]
            self.board[robot[0]][robot[1]] = '0'
            new_pos = (robot[0], robot[1] - 1)
        return new_pos

    def slideAway(self, robot: tuple, dir: str):
        aux = self.swapPos((robot[0], robot[1]), dir)
        if aux == (-1, -1):
            self.robotOnTarget = (self.targetPos == robot and self.targetColor == self.board[robot[0]][robot[1]])
            return
        self.slideAway(aux, dir)

    def robot_position(self, robot: str):
        a = np.array(self.board)
        result = np.where(a == robot)
        coor = list(zip(result[0] + 1, result[1] + 1))
        return coor[0]

    def getDistance(self, pos1: tuple, pos2: tuple):
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        bias = abs(dx - dy)
        manhattan_distance = dx + dy
        return manhattan_distance + bias

def parse_instance(filename: str) -> Board:
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

class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = RRState(board)

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions = []
        for robot in ['R', 'G', 'B', 'Y']:
            pos = state.board.robot_position(robot)
            for dir in ['u', 'd', 'l', 'r']:
                if state.board.swapPos((pos[0] - 1, pos[1] - 1), dir) != (-1, -1):
                    if dir == 'u':
                        state.board.swapPos((pos[0] - 2, pos[1] - 1), 'd')
                    elif dir == 'd':
                        state.board.swapPos((pos[0], pos[1] - 1), 'u')
                    elif dir == 'l':
                        state.board.swapPos((pos[0] - 1, pos[1] - 2), 'r')
                    elif dir == 'r':
                        state.board.swapPos((pos[0] - 1, pos[1]), 'l')
                    actions.append((robot, dir))
        return actions

    def copyMatrix(self, inputList):
        res = []
        for x in range(len(inputList)):
            temp = []
            for elem in inputList[x]:
                temp.append(elem)
            res.append(temp)
        return res
    
    def copyList(self, inputList):
        res = []
        for x in inputList:
            res.append(x)
        return res

    def cloneState(self, state: RRState):
        new_repr = self.copyMatrix(state.board.board)
        new_internal_walls = self.copyMatrix(state.board.internal_walls)
        new_board = Board(state.board.size)
        new_board.board = new_repr
        new_board.internal_walls = new_internal_walls
        new_board.robotOnTarget = state.board.robotOnTarget
        new_board.targetColor = state.board.targetColor
        new_board.targetPos = state.board.targetPos
        new_state = RRState(new_board)
        new_state.id = state.id
        return new_state
    
    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        new_state = self.cloneState(state)
        robot_pos = new_state.board.robot_position(action[0])
        new_state.board.slideAway((robot_pos[0] - 1, robot_pos[1] - 1), action[1])
        return new_state

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        return state.board.robotOnTarget

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        #sum of manhattan distance of all robots + bias:
        robot_pos1 = node.state.board.robot_position('G')
        robot_pos2 = node.state.board.robot_position('R')
        robot_pos3 = node.state.board.robot_position('Y')
        robot_pos4 = node.state.board.robot_position('B')
        return node.state.board.getDistance(robot_pos1, node.state.board.targetPos) + node.state.board.getDistance(robot_pos2, node.state.board.targetPos) + node.state.board.getDistance(robot_pos3, node.state.board.targetPos) + node.state.board.getDistance(robot_pos4, node.state.board.targetPos)

    def output(self, node: Node):
        actions = node.solution()
        print(len(actions))
        for action in actions:
            print(action[0] + " " + action[1])

if __name__ == "__main__":
    # Ler o ficheiro de input de sys.ar gv[1],
    board = parse_instance(sys.argv[1])
    # Usar uma técnica de procura para resolver a instância,
    problem = RicochetRobots(board)
    inst = InstrumentedProblem(problem)
    # Retirar a solução a partir do nó resultante,
    start = time.time()
    #solution_node = astar_search(inst)
    solution_node = breadth_first_tree_search(inst)
    end = time.time()
    print(end - start)
    #print(len(solution_node.path()))
    #print(len(solution_node.expand(problem)))
    #states = gerados, succs = expandidos, goal_tests = testados como solução
    print("expandidos: ", inst.states)
    print("gerados: ", inst.succs)
    # Imprimir para o standard output no formato indicado.
    #problem.output(solution_node)