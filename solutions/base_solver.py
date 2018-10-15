#-*- coding:utf-8 -*-
class Solution:
    def get_name(self):
        raise Exception('implements')

    def solve(self, init_state):
        raise Exception('implements')

    def restart(self):
        pass

    @staticmethod
    def get_value(state, slot_number):
        return state[slot_number//3, slot_number%3]

    @staticmethod
    def set_value(state, slot_number, turn):
        state[slot_number // 3, slot_number % 3] = turn

