#-*- coding:utf-8 -*-
import numpy as np
import random
from solutions.Heuristic import Heuristic


class GameMgr:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.win = 0
        self.lose = 0
        self.solver = Heuristic(depth=4)

    def start(self):
        self.board = np.zeros((3, 3))
        self.solver.restart()

    # 플레이어 착수 & 컴퓨터 착수 & 승패무 여부 계산
    # 반환값: (승패여부, 컴퓨터가 둔 슬롯 넘버(-1이면 안둠))
    #   승패여부: {0: 안끝, 1: 플레이어승, -1: 컴퓨터승, -2:무승부}
    def go(self, p_slot):
        if self.get_value(p_slot) != 0:  # 해당 부분이 이미 선택되어 있다면 오류.
            raise Exception('wrong slot')

        self.set_value(p_slot, 'p')  # 플레이어 착수
        result = self.end_inspection()  # 승리/무승부 검사
        if result == 1: # 승리 시
            return 1, -1
        elif result == -2: # 무승부 시
            return -2, -1

        c_slot = self.solver.solve(self.board)
        self.set_value(c_slot, 'c')  # 컴퓨터 착수
        result = self.end_inspection()  # 패배/무승부 검사
        return result, c_slot

    # 판이 끝났는 지 검사. 0: 안끝, 1: 플레이어승, -1: 컴퓨터승, -2:무승부
    def end_inspection(self):
        nd = 0  # \ 대각선
        pd = 0  # / 대각선

        for i in range(3):
            nd += self.board[i, i]
            pd += self.board[2-i, i]
            row_result = self.board[i, :].sum()
            col_result = self.board[:, i].sum()
            if row_result == 3 or col_result == 3:
                self.win += 1
                #print('win: {}.row:{}, {}.col:{}'.format(i, row_result, i, col_result))
                return 1
            elif row_result == -3 or col_result == -3:
                self.lose += 1
                #print('lose: {}.row:{}, {}.col:{}'.format(i, row_result, i, col_result))
                return -1

        if nd == 3 or pd == 3:
            self.win += 1
            return 1
        elif nd == -3 or pd == -3:
            self.lose += 1
            return -1

        if (self.board == 0).sum() == 0:  # 모든 칸이 다 차면 무승부
            return -2
        return 0

    # 판에 해당하는 값을 반환 (0은 공백, 1은 플레이어, c:2는 컴퓨터)
    def get_value(self, slot_number):
        return self.board[slot_number//3, slot_number%3]

    # 판에 수를 둠 (p:1은 플레이어, c:2는 컴퓨터)
    def set_value(self, slot_number, turn):
        if turn == 'p':
            self.board[slot_number // 3, slot_number % 3] = 1
        elif turn == 'c':
            self.board[slot_number // 3, slot_number % 3] = -1
        else:
            raise Exception("wrong turn str")