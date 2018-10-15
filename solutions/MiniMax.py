#-*- coding:utf-8 -*-
from solutions.base_solver import Solution
import numpy as np
import pickle
import os.path
import time

CHKECK = False

class MiniMaxTree(object):
    def __init__(self, state, action=None, turn=None):
        assert isinstance(state, np.ndarray)
        self.state = state
        self.action = action
        self.children = []
        self.reward = None
        self.turn = turn  # -1: 내턴(컴퓨터), 1:상대턴(유저)

    def add_child(self, node):
        assert isinstance(node, MiniMaxTree)
        self.children.append(node)

    def set_reward(self, reward):
        assert isinstance(reward, int) or isinstance(reward, np.int32)
        self.reward = reward

class MiniMax(Solution):
    def __init__(self, first='p', tree_file='./solutions/minimax.pk'):
        init_state = np.zeros((3, 3))

        if os.path.exists(tree_file):
            st = time.time()
            with open(tree_file, 'rb') as f:
                self.root = pickle.load(f)
            print('load tree time:', str(time.time() - st)[:4])
        else:
            st = time.time()
            self.root = MiniMaxTree(init_state, turn=1)
            self.make_tree(self.root)
            print('make tree time:', str(time.time()-st)[:4])
            with open(tree_file, 'wb') as f:
                pickle.dump(self.root, f)

        self.current_root = self.root

        if CHKECK:
            print('root:', self.root.state)
            for i, child in enumerate(self.root.children):
                print('child_{}:'.format(i), child.state)

    def restart(self):
        self.current_root = self.root

    def make_tree(self, node):
        state = node.state
        turn = node.turn

        reward = self.end_inspection(state)
        if reward != 0:
            node.set_reward(reward)
            return reward

        child_values = []
        # 자식 노드 생성
        for i in range(9):
            if self.get_value(state, i) != 0:
                continue
            ch_state = state.copy()
            self.set_value(ch_state, i, turn)  # 상태 변환
            child = MiniMaxTree(ch_state, action=i, turn=-turn)  # 노드 생성
            ch_value = self.make_tree(child)  # 트리 생성 및 가치값 확인
            child_values.append(ch_value)
            node.add_child(child)  # 자식 노드 등록

        if turn == -1:  # 컴퓨터 차례라면
            reward = np.max(child_values)
        else:  # 유저 차례라면
            reward = np.min(child_values)
        node.set_reward(reward)
        return reward

    def solve(self, init_state):
        self.update_root(init_state)  # 상대가 변경한 상태를 Tree에서 찾음
        next_node = self.find_best_node()  # 현재 root에서의 최적해를 구함
        self.current_root = next_node  # 행동할 상태로 root를 옮김

        return next_node.action  # 최적해의 액션(선택할 슬롯번호) 출력

    # 변경된 상태와 일치하는 노드를 찾고, 루트 노트로 변경함
    def update_root(self, state):
        children = self.current_root.children
        for child in children:
            if np.array_equal(child.state, state):
                self.current_root = child
                return
        print('no!')
        raise Exception('Can\'t find child')

    def find_best_node(self):
        ch_rewards = []
        for child in self.current_root.children:
            ch_rewards.append(child.reward)
        idx = np.argmax(ch_rewards)
        return self.current_root.children[idx]

    # 판이 끝났는 지 검사. 0: 안끝, 999: 컴퓨터승, -999: 플레이어승, -1:무승부
    @staticmethod
    def end_inspection(state):
        nd = 0  # \ 대각선
        pd = 0  # / 대각선

        for i in range(3):
            nd += state[i, i]
            pd += state[2-i, i]
            row_result = state[i, :].sum()
            col_result = state[:, i].sum()
            if row_result == 3 or col_result == 3:
                return -999
            elif row_result == -3 or col_result == -3:
                return 999

        if nd == 3 or pd == 3:
            return -999
        elif nd == -3 or pd == -3:
            return 999

        if (state == 0).sum() == 0:  # 모든 칸이 다 차면 무승부
            return -1
        return 0


    def get_name(self):
        return 'MiniMax'

