import argparse

from flask import Flask, jsonify, request

from lib.cpu import *

app = Flask(__name__)


@app.route('/cpu', methods=['GET'])
def cpu_state():
    # 读取URL的参数
    interval = request.args.get('interval', type=Union[float, None])
    percpu = request.args.get('percpu', type=bool)
    fahrenheit = request.args.get('fahrenheit', type=bool)

    state = get_cpu_state(interval, percpu)
    res = {
        'cpu_usage': state['cpu_usage'],
        'cpu_freq': state['cpu_freq'],
        'cpu_cores': state['cpu_cores'],
        'cpu_ctx_switches': state['cpu_ctx_switches'],
        'cpu_interrupts': state['cpu_interrupts'],
        'cpu_soft_interrupts': state['cpu_soft_interrupts'],
        'cpu_syscalls': state['cpu_syscalls'],
        'cpu_temp': get_cpu_temperature(fahrenheit),
    }

    return jsonify(res)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', type=bool, default=False, help='是否开启调试模式')

    args = parser.parse_args()
    app.run(debug=args.debug)
