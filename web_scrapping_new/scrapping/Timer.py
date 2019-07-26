import threading
import time

class RepeatEvery(threading.Thread):
    def __init__(self, interval, func, *args):
        threading.Thread.__init__(self)
        self.interval = interval  # seconds between calls
        self.func = func          # function to call
        self.args = args          # optional positional argument(s) for call
        self.runable = True
    def run(self):
        while self.runable:
            self.func(*self.args)
            time.sleep(self.interval)
    def stop(self):
        self.runable = False

if __name__ == "__main__":

    def hello():
        print('hello')

    s = RepeatEvery(10,hello)
    s.run()