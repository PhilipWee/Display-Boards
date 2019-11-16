from threading import Thread,Timer
from lib import DisplayBoard as displayBoard
from datetime import datetime
import time

class RealClock(Thread):

    def __init__(self,stopThread,stopTimer):
        Thread.__init__(self)
        self.stopThread = stopThread
        self.stopTimer = stopTimer

    def run(self):         
        while True:    
            if self.stopThread.is_set():
                break
            if not self.stopTimer.wait(1.0):
                displayBoard.display_time()

class EventTimer(Thread):
    def __init__(self,event,event_set=False,interval=10):
        Thread.__init__(self)
        self.event = event
        self.interval = interval
        self.event_set = event_set

    def run(self):         
        time.sleep(self.interval)
        if self.event_set:
            self.event.set()
        else:
            self.event.clear()


