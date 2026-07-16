from multiprocessing import Process
import time


class MyProcess(Process):
    def __init__(self, loop):
        Process.__init__(self)
        self.loop = loop

    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            print(f'Pid: {self.pid} LoopCount: {count}')


if __name__ == "__main__":
    process = []
    for i in range(2, 5):
        p = MyProcess(i)
        process.append(p)
        p.daemon = True
        p.start()
    for p in process:
        p.join()


    print('Main Process ended') 