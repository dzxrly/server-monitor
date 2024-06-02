import time

from lib.cpu import *

if __name__ == '__main__':
    while True:
        print(get_cpu_state(
            interval=None,
            percpu=True,
        ))
        print(get_cpu_temperature(
            fahrenheit=False
        ))
        time.sleep(3)
