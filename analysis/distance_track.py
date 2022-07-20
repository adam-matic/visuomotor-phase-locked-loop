from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time, json, scipy, sys
import numpy as np
import random
from trajectory_analysis import Trajectory
from generate_disturbance import pseudorandom


class TargetTrackingWindow(QWidget):
    def __init__(self, parent=None):
        super(TargetTrackingWindow, self).__init__(parent)
        self.setCursor(Qt.BlankCursor)
        width, height = 1200, 800
        self.resize(width, height)
        self.setWindowTitle("Target tracking experiment")
        self.setMouseTracking(True)

        self.dt = 1.0 / 60.0
        self.cnt = 0

        self.duration = 60
        self.N = int(self.duration / self.dt)
        self.difficulty = 80
        self.target_xs = pseudorandom(n=self.difficulty, duration=self.duration, range_from=100, range_to=1100, dt=self.dt, seed=73)
        self.target_ys = pseudorandom(n=self.difficulty, duration=self.duration, range_from=100, range_to=700, dt=self.dt, seed=75)

        self.target_x = self.target_xs[0]
        self.target_y = self.target_ys[0]
        
        self.task = f"random, difficulty {self.difficulty}"
        
        self.times=[]
        self.tstart = time.perf_counter()
        self.t0 = self.tstart
        
        self.show()
        m0 = self.mapFromGlobal(QCursor.pos())        
        self.mouse_x = m0.x()
        self.mouse_y = m0.y()
        
        self.tts = []  # time 
        self.txs = []  # target x
        self.tys = []  # target y
        self.cxs = []  # cursor x  
        self.cys = []  # cursor y   

        self.tick_timer = QTimer(self)
        self.tick_timer.singleShot(15, self.tick)
    

    def tick(self):
        if self.cnt+1 < self.N: 
            t1 = time.perf_counter() 
            while (t1 - self.t0) < 0.016666:
                t1 = time.perf_counter()
                QApplication.processEvents()
            self.tick_timer.singleShot(15, self.tick) 
            self.t0 = t1

            t = t1 - self.tstart
            self.target_x = self.target_xs[self.cnt]
            self.target_y = self.target_ys[self.cnt]
            self.txs.append(self.target_x)
            self.tys.append(self.target_y)
            self.tts.append(t)
            self.cxs.append(self.mouse_x)
            self.cys.append(self.mouse_y)
            self.cnt += 1        
            self.repaint()

        else:
            self.save_data()
            self.close()
            print("Done, closing")
            print("Frame time mean and stdev:")
            print(np.mean(np.diff(self.times)))
            print(np.std(np.diff(self.times)))


    def save_data(self):
        d = { "tts": self.tts, 
              "txs": self.txs,
              "tys": self.tys, 
              "cxs": self.cxs,
              "cys": self.cys }

        t = time.time()
        t_stamp = time.ctime(t).replace(":", "-")
        self.fname = f"{self.task} {t_stamp}.json"
        json.dump(d, open(self.fname, "w"))
        print("Saved as: ", self.fname)
                        

    def mouseMoveEvent(self, event):
        self.mouse_x = event.x()
        self.mouse_y = event.y()

    def paintEvent(self, event):
        self.times.append(time.perf_counter())
        painter = QPainter(self)

        painter.setBrush(QBrush( Qt.green, Qt.SolidPattern))
        painter.drawEllipse(self.mouse_x, self.mouse_y, 9, 9)

        painter.setBrush(QBrush( Qt.red, Qt.SolidPattern))
        painter.drawEllipse(int(self.target_x), int(self.target_y), 5, 5)

    

app = QApplication(sys.argv)
m = TargetTrackingWindow()
m.show()
app.exec_()