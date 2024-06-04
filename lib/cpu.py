from typing import Optional

import psutil


def get_cpu_state(
        interval: float = None,
        percpu: bool = False,
) -> dict:
    """
    获取CPU的各种状态
    :param interval: 间隔时间，单位秒；默认None，即获取与上次调用之间的CPU使用率
    :param percpu: 是否获取每个CPU的使用率(逻辑核心)，默认False
    :return: 返回CPU状态
    """
    try:
        cpu_stats = psutil.cpu_stats()
        return {
            'cpuUsage': {
                'percpu': psutil.cpu_percent(interval=interval, percpu=percpu),
                'avg': psutil.cpu_percent(interval=interval, percpu=False),
            },
            'cpuFreq': {
                'percpu': [
                    {
                        'current': freq.current,
                        'min': freq.min,
                        'max': freq.max,
                    } for freq in psutil.cpu_freq(percpu=True)
                ],
                'avg': {
                    'current': psutil.cpu_freq(percpu=False).current,
                    'min': psutil.cpu_freq(percpu=False).min,
                    'max': psutil.cpu_freq(percpu=False).max,
                },
            },
            'cpuCores': {
                'cores': psutil.cpu_count(logical=False),
                'threads': psutil.cpu_count(logical=True),
            },
            'cpuCTXSwitches': cpu_stats.ctx_switches,
            'cpuInterrupts': cpu_stats.interrupts,
            'cpuSoftInterrupts': cpu_stats.soft_interrupts,
            'cpuSyscalls': cpu_stats.syscalls,
        }
    except Exception as e:
        raise '[ERROR] Get CPU state failed. Detail: {}'.format(e)


def get_cpu_temperature(
        fahrenheit: bool = False,
) -> Optional[dict]:
    """
    获取CPU温度，仅在Linux下有效
    :param fahrenheit: 是否返回华氏温度，否则返回摄氏温度；默认False
    :return: 返回CPU温度
    """
    try:
        temps = psutil.sensors_temperatures(fahrenheit=fahrenheit)
        if 'coretemp' in temps:
            return {
                'numaNodeTemperature': [
                    {
                        'label': temp.label,
                        'current': temp.current,
                        'high': temp.high,
                        'critical': temp.critical,
                    } for temp in temps['coretemp'] if 'Package id' in temp.label
                ],
                'coreTemperature': [
                    {
                        'label': temp.label,
                        'current': temp.current,
                        'high': temp.high,
                        'critical': temp.critical,
                    } for temp in temps['coretemp'] if 'Core' in temp.label
                ],
            }
        else:
            return {}
    except Exception as e:
        raise '[ERROR] Get CPU temperature failed. Detail: {}'.format(e)


def get_cpu_name() -> str:
    """
    获取CPU名称，仅在Linux和Windows下有效
    :return: 返回CPU名称，如果获取失败则返回'Unknown'
    """
    if psutil.LINUX:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f.readlines():
                if 'model name' in line:
                    return line.split(':')[1].strip()
        return 'Unknown'
    elif psutil.WINDOWS:
        try:
            import wmi
            c = wmi.WMI()
            return c.Win32_Processor()[0].Name
        except Exception as e:
            return 'Unknown'
    else:
        raise NotImplementedError('Unsupported system')
