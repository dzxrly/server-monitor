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
            'memory_total': unit_convert(mem.total, 'B', unit),
            'memory_available': unit_convert(mem.available, 'B', unit),
            'memory_used': unit_convert(mem.used, 'B', unit),
            'memory_free': unit_convert(mem.free, 'B', unit),
            'memory_percent': mem.percent,
            'swap_total': unit_convert(swap.total, 'B', unit),
            'swap_used': unit_convert(swap.used, 'B', unit),
            'swap_free': unit_convert(swap.free, 'B', unit),
            'swap_percent': swap.percent,
        }
    except Exception as e:
        return {}
