#-*- coding:utf-8 -*-
from solutions.base_solver import Solution
import random


class RandomSelection(Solution):
    def solve(self, init_state, limit=1000):
        count = 0
        while True:
            select = random.randint(0, 8)  # [0, 9) 선택
            if self.get_value(init_state, select) == 0:
                return select
            count += 1
            if count > limit:
                raise Exception('exceed limit')

    def get_name(self):
        return 'RandomSelection'

