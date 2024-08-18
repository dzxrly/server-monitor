from lib.utils.utils import unit_convert, temperature_convert


def get_nv_gpu_state(
        unit: str = 'GB',
        fahrenheit: bool = False,
) -> dict:
    """
    获取NVIDIA GPU的状态，包括GPU的名称、总内存、已用内存、剩余内存、内存使用率
    :param unit: 内存的单位，可选值为B, KB, MB, GB, TB
    :param fahrenheit: 是否使用华氏度
    :return: dict
    """

    assert unit in ['B', 'KB', 'MB', 'GB', 'TB'], NotImplementedError(
        'Only support B, KB, MB, GB, TB. Got {}'.format(unit))

    try:
        import pynvml
        pynvml.nvmlInit()
        res = {
            'driverVersion': pynvml.nvmlSystemGetDriverVersion(),
            'gpuList': [],
        }
        for device_index in range(pynvml.nvmlDeviceGetCount()):
            handle = pynvml.nvmlDeviceGetHandleByIndex(device_index)
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            usage_info = pynvml.nvmlDeviceGetUtilizationRates(handle)
            fan_speed = 0
            try:
                fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
            except pynvml.NVMLError:
                pass
            res['gpuList'].append({
                'gpuIndex': device_index,
                'gpuName': pynvml.nvmlDeviceGetName(handle),
                'gpuUsage': usage_info.gpu,
                'memoryTotal': unit_convert(memory_info.total, 'B', unit),
                'memoryUsed': unit_convert(memory_info.used, 'B', unit),
                'memoryFree': unit_convert(memory_info.free, 'B', unit),
                'memoryPercent': memory_info.used / memory_info.total * 100,
                'gpuTemperature': temperature_convert(
                    pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU),
                    'C',
                    'F' if fahrenheit else 'C',
                ),
                'powerCurrent': pynvml.nvmlDeviceGetPowerUsage(handle) / 1000,
                'powerLimit': pynvml.nvmlDeviceGetEnforcedPowerLimit(handle) / 1000,
                'fanSpeed': fan_speed,
            })
        pynvml.nvmlShutdown()
        return res
    except NotImplementedError as e:
        raise '[ERROR] Only support NVIDIA GPU. Detail: {}'.format(e)
