#-*- coding: UTF-8 -*-

import os
from game_mgr import GameMgr
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
import sys

PRINT_LOG = False


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class GameGUI(QMainWindow):
    def __init__(self, mgr, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = loadUi(resource_path("./3x3_game.ui"), self)
        self.setWindowTitle('3x3 game')
        self.ui.show()

        self.mgr = mgr  # 게임 매니저
        self.setEvent()  # 각 슬롯에 이벤트 초기화

        self.iconO = QIcon(resource_path('icon/1.png'))  # O 그림
        self.iconX = QIcon(resource_path('icon/2.png'))  # X 그림

    def setEvent(self, n_slot=9):
        for i in range(n_slot):
            bt_slot = self.ui.findChild(QPushButton, "slot_{}".format(i))
            bt_slot.clicked.connect(self.slotEvent(i, bt_slot))
            bt_slot.setIconSize(bt_slot.size())

    @pyqtSlot()
    def start_game(self):
        self.mgr.start()
        self.ui.bt_start.setText("restart")
        for i in range(9):
            bt_slot = self.ui.findChild(QPushButton, "slot_{}".format(i))
            bt_slot.setEnabled(True)
            bt_slot.setIcon(QIcon())

    def select_slot(self, number, turn='p'):
        bt = self.ui.findChild(QPushButton, "slot_{}".format(number))

        #bt = self.ui.slot_0
        if turn == 'p':
            bt.setIcon(self.iconO)
        else:
            bt.setIcon(self.iconX)
        bt.setEnabled(False)

    def slotEvent(self, number, bt):
        def Event():
            if PRINT_LOG:
                print('clicked slot_{}'.format(number))
            self.select_slot(number, 'p')
            result, c_slot = self.mgr.go(number)
            if c_slot != -1:  # 컴퓨터가 착수한 경우에만 둠
                self.select_slot(c_slot, 'c')
            if result != 0:
                self.end_game(result)

        return Event

    # 게임 종료 및 결과 출력
    def end_game(self, result):
        # 모든 슬롯 무효화
        for i in range(9):
            bt_slot = self.ui.findChild(QPushButton, "slot_{}".format(i))
            bt_slot.setEnabled(False)

        # 점수판 갱신
        self.ui.la_win.setText(str(self.mgr.win))
        self.ui.la_lose.setText(str(self.mgr.lose))

        if result == 1:
            QMessageBox.about(self, " ", "플레이어 승")
        elif result == -1:
            QMessageBox.about(self, " ", "컴퓨터 승")
        elif result == -2:
            QMessageBox.about(self, " ", "무승부")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mgr = GameMgr()  # 게임 매니저 생성
    w = GameGUI(mgr)  # GUI 실행
    sys.exit(app.exec())