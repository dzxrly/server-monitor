import psutil

from lib.utils.utils import unit_convert


def get_memory_state(
        unit: str = 'GB',
) -> dict:
    """
    获取内存的状态，包括总内存、可用内存、已用内存、剩余内存、内存使用率，以及交换分区的状态
    :param unit: 内存的单位，可选值为B, KB, MB, GB, TB
    :return: dict
    """
    assert unit in ['B', 'KB', 'MB', 'GB', 'TB'], \
        '[ERROR] get_memory_state: unit must be one of B, KB, MB, GB, TB'

    try:
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            'memoryTotal': unit_convert(mem.total, 'B', unit),
            'memoryAvailable': unit_convert(mem.available, 'B', unit),
            'memoryUsed': unit_convert(mem.used, 'B', unit),
            'memoryFree': unit_convert(mem.free, 'B', unit),
            'memoryPercent': mem.percent,
            'swapTotal': unit_convert(swap.total, 'B', unit),
            'swapUsed': unit_convert(swap.used, 'B', unit),
            'swapFree': unit_convert(swap.free, 'B', unit),
            'swapPercent': swap.percent,
        }
    except Exception as e:
        raise '[ERROR] get_memory_state: {}'.format(e)
