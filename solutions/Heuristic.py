#-*- coding:utf-8 -*-
from solutions.base_solver import Solution
import numpy as np

WIN = 999  # 컴퓨터 기준
LOSE = -999
DRAW = -10


class Heuristic(Solution):
    def __init__(self, depth=3):
        self.depth = depth  # depth 무한 시, minimax와 동일

    def find_best(self, state, turn, depth=1):
        # 주어진 상태에서의 최적해를 계산 (재귀함수)
        reward = self.evaluate_state(state)  # 현재 상태의 평가값 검사
        if reward == WIN or reward == LOSE or reward == DRAW:
            if reward == WIN:
                return -1, reward - depth  # depth가 깊을 수록 페널티
            else:
                return -1, reward + depth  # depth가 깊을 수록 어드밴티지
        if depth > self.depth:  # 깊이 제한 시, heuristic 함수값
            return -1, reward
        # 주어진 상태에서 게임이 끝나지 않고, 깊이 제한에 걸리지 않는다면, 자식 노드 확장

        ch_actions, ch_rewards = [], []
        # 자식 노드 생성
        for i in range(9):  # 가능한 action 조회 (action에 따른 자식 노드를 생성)
            if self.get_value(state, i) != 0:  # 이미 해당 슬롯에 값이 채워져있으면 통과
                continue
            ch_state = state.copy()
            self.set_value(ch_state, i, turn)  # 상태 변환 (i가 곧 action)
            _, ch_reward = self.find_best(ch_state, -turn, depth+1)  # 자식 노드의 평가값 판별
            ch_actions.append(i)
            ch_rewards.append(ch_reward)

        if turn == -1:  # 컴퓨터(자신) 차례라면 최대값 선택
            idx = np.argmax(ch_rewards)
        else:  # 유저(상대) 차례라면 최소값 선택
            idx = np.argmin(ch_rewards)
            
        return ch_actions[idx], ch_rewards[idx]

    def solve(self, init_state):
        # 주어진 상태에 대한 최적 action 출력
        # init_state : (3,3) [0:공백, -1:컴퓨터, 1:사람]
        action, _ = self.find_best(init_state, turn=-1)
        return action  # 최적해의 액션(선택할 슬롯번호) 출력

    @staticmethod
    def evaluate_state(state):
        # 상태 평가 함수 (게임 승패 여부 및, heuristic 방법에 따라 평가값 출력)
        # state : (3,3) [0:공백, -1:컴퓨터, 1:사람]
        reward = 0  # 평가값
        nd_sum = 0  # \ 대각선에 값이 채워진 수
        pd_sum = 0  # / 대각선에 값이 채워진 수
        nd_count = 0  # \ 대각선 값 합산
        pd_count = 0  # / 대각선 값 합산
        
        for i in range(3):
            if state[i, i] != 0:
                nd_sum += state[i, i]
                nd_count += 1
            if state[2-i, i] != 0:
                pd_sum += state[2-i, i]
                pd_count += 1
            row = state[i, :]
            col = state[:, i]
            row_sum = row.sum()
            col_sum = col.sum()

            # 한 줄이 같은 값으로 차면 승리 혹은 패배 (행, 열)
            if row_sum == 3 or col_sum == 3:
                return LOSE
            elif row_sum == -3 or col_sum == -3:
                return WIN

            # heuristic method 값 계산 (행, 열)
            if row_sum != 0 and (row == 0).sum() != 3:  # 행 검사
                # 모든 값이 공백이 아니고, 하나 이상의 공백이 있을 때
                reward += (-1 if row_sum > 0 else 1)
            if col_sum != 0 and (col == 0).sum() != 3:  # 열 검사
                reward += (-1 if col_sum > 0 else 1)

        # 한 줄이 같은 값으로 차면 승리 혹은 패배 (대각선)
        if nd_sum == 3 or pd_sum == 3:
            return LOSE
        elif nd_sum == -3 or pd_sum == -3:
            return WIN

        # 모든 칸이 다 차면 무승부
        if (state == 0).sum() == 0:
            return DRAW

        # heuristic method 값 계산 (대각선)
        if nd_count != 3:
            reward += (-1 if nd_sum > 0 else 1)
        if pd_count != 3:
            reward += (-1 if pd_sum > 0 else 1)
                
        return reward

    def get_name(self):
        return 'Heuristic'

