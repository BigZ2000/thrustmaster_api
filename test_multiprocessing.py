from multiprocessing import Process
import os
from simple_joystick import thrusmaster_handle
import time

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=thrusmaster_handle, args=('kakiri-robot.local', 9090, 'vesc/cmd_vel',))
    p.start()
    pid = p.pid
    print('process.pid of the processus function', pid)
    print('os.getpid() of the main function', os.getpid())
    time.sleep(5)
    p.kill()
    p.join()
    time.sleep(5)
    p = Process(target=thrusmaster_handle, args=('kakiri-robot.local', 9090, 'vesc/cmd_vel',))
    pid = p.pid
    print('process.pid of the processus function', pid)
    p.start()
    print('os.getpid() of the main function', os.getpid())
    time.sleep(5)
    p.kill()
    p.join()
    