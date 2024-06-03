import argparse
from typing import Union

from flask import Flask, jsonify, request, abort

from lib.cpu import get_cpu_state, get_cpu_temperature, get_cpu_name
from lib.gpu import get_nv_gpu_state
from lib.memory import get_memory_state
from lib.utils.utils import flask_request_arg_bool

app = Flask(__name__)


@app.route('/cpu_name', methods=['GET'])
def cpu_name():
    try:
        return jsonify({
            'cpu_name': get_cpu_name(),
        })
    except Exception as e:
        return jsonify({
            'cpu_name': 'Unknown',
        })


@app.route('/cpu_state', methods=['GET'])
def cpu_state():
    # 读取URL的参数
    interval = request.args.get('interval', type=Union[float, None])
    percpu = request.args.get('percpu', type=flask_request_arg_bool)
    fahrenheit = request.args.get('fahrenheit', type=flask_request_arg_bool)

    state = get_cpu_state(interval, percpu)
    res = {
        'cpu_usage': state['cpu_usage'],
        'cpu_freq': state['cpu_freq'],
        'cpu_cores': state['cpu_cores'],
        'cpu_ctx_switches': state['cpu_ctx_switches'],
        'cpu_interrupts': state['cpu_interrupts'],
        'cpu_soft_interrupts': state['cpu_soft_interrupts'],
        'cpu_syscalls': state['cpu_syscalls'],
        'cpu_temperature': get_cpu_temperature(fahrenheit),
    }

    return jsonify(res)


@app.route('/memory', methods=['GET'])
def memory_state():
    # 读取URL的参数
    unit = request.args.get('unit', type=str)

    try:
        state = get_memory_state(unit)
        return jsonify({
            'memory_total': state['memory_total'],
            'memory_available': state['memory_available'],
            'memory_used': state['memory_used'],
            'memory_free': state['memory_free'],
            'memory_percent': state['memory_percent'],
            'swap_total': state['swap_total'],
            'swap_used': state['swap_used'],
            'swap_free': state['swap_free'],
            'swap_percent': state['swap_percent'],
        })
    except Exception as e:
        abort(400)


@app.route('/gpu_state', methods=['GET'])
def get_gpu_state():
    # 读取URL的参数
    unit = request.args.get('unit', type=str)
    fahrenheit = request.args.get('fahrenheit', type=flask_request_arg_bool)
    print(unit, fahrenheit)

    try:
        gpu_state = get_nv_gpu_state(unit=unit, fahrenheit=fahrenheit)
        return jsonify({
            'driver_version': gpu_state['driver_version'],
            'gpu_list': gpu_state['gpu_list'],
        })
    except Exception as e:
        abort(400)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', type=bool, default=False, help='是否开启调试模式')

    args = parser.parse_args()
    app.run(debug=args.debug, host='0.0.0.0')
