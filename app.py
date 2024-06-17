from typing import Union

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from lib.cpu import get_cpu_state, get_cpu_temperature, get_cpu_name
from lib.gpu import get_nv_gpu_state
from lib.memory import get_memory_state
from lib.network import get_net_state
from lib.utils.utils import flask_request_arg_bool

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/cpu_name', methods=['GET'])
def cpu_name():
    try:
        return jsonify({
            'cpuName': get_cpu_name(),
        })
    except Exception as e:
        return jsonify({
            'cpuName': 'Unknown',
        })


@app.route('/cpu_state', methods=['GET'])
def cpu_state():
    # 读取URL的参数
    interval = request.args.get('interval', type=Union[float, None])
    percpu = request.args.get('percpu', type=flask_request_arg_bool)
    fahrenheit = request.args.get('fahrenheit', type=flask_request_arg_bool)

    state = get_cpu_state(interval, percpu)
    res = {
        'cpuUsage': state['cpuUsage'],
        'cpuFreq': state['cpuFreq'],
        'cpuCores': state['cpuCores'],
        'cpuCTXSwitches': state['cpuCTXSwitches'],
        'cpuInterrupts': state['cpuInterrupts'],
        'cpuSoftInterrupts': state['cpuSoftInterrupts'],
        'cpuSyscalls': state['cpuSyscalls'],
        'cpuTemperature': get_cpu_temperature(fahrenheit),
    }

    return jsonify(res)


@app.route('/memory_state', methods=['GET'])
def memory_state():
    # 读取URL的参数
    unit = request.args.get('unit', type=str)

    try:
        state = get_memory_state(unit)
        return jsonify({
            'memoryTotal': state['memoryTotal'],
            'memoryAvailable': state['memoryAvailable'],
            'memoryUsed': state['memoryUsed'],
            'memoryFree': state['memoryFree'],
            'memoryPercent': state['memoryPercent'],
            'swapTotal': state['swapTotal'],
            'swapUsed': state['swapUsed'],
            'swapFree': state['swapFree'],
            'swapPercent': state['swapPercent'],
        })
    except Exception as e:
        abort(400)


@app.route('/gpu_state', methods=['GET'])
def get_gpu_state():
    # 读取URL的参数
    unit = request.args.get('unit', type=str)
    fahrenheit = request.args.get('', type=flask_request_arg_bool)

    try:
        gpu_state = get_nv_gpu_state(unit=unit, fahrenheit=fahrenheit)
        return jsonify({
            'driverVersion': gpu_state['driverVersion'],
            'gpuList': gpu_state['gpuList'],
        })
    except Exception as e:
        abort(400)


@app.route('/network_state', methods=['GET'])
def get_network_state():
    # 读取URL的参数
    unit = request.args.get('unit', type=str)

    try:
        network_state = get_net_state(unit=unit)
        return jsonify(network_state)
    except Exception as e:
        abort(400)
