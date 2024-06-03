import psutil


def unit_convert(
        input_value: float,
        input_unit: str,
        output_unit: str,
) -> float:
    assert input_unit in ['B', 'KB', 'MB', 'GB', 'TB'], \
        '[ERROR] unit_convert: input_unit must be one of B, KB, MB, GB, TB'
    assert output_unit in ['B', 'KB', 'MB', 'GB', 'TB'], \
        '[ERROR] unit_convert: output_unit must be one of B, KB, MB, GB, TB'

    unit_dict = {
        'B': 0,
        'KB': 1,
        'MB': 2,
        'GB': 3,
        'TB': 4,
    }

    return input_value * (1024 ** (unit_dict[input_unit] - unit_dict[output_unit]))


def get_memory_state(
        unit: str = 'GB',
) -> dict:
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
