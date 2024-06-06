import psutil

from lib.utils.utils import unit_convert


def get_net_state(
        unit: str = 'MB',
) -> dict:
    """
    获取网络状态
    :param unit: 网络状态的单位，可选值为B, KB, MB, GB, TB
    :return: 返回网络状态
    """
    assert unit in ['B', 'KB', 'MB', 'GB', 'TB'], NotImplementedError(
        'Only support B, KB, MB, GB, TB. Got {}'.format(unit))

    net_state = psutil.net_io_counters(pernic=False, nowrap=True)
    return {
        'bytesSent': unit_convert(net_state.bytes_sent, 'B', unit),
        'bytesRecv': unit_convert(net_state.bytes_recv, 'B', unit),
        'packetsSent': net_state.packets_sent,
        'packetsRecv': net_state.packets_recv,
        'errIn': net_state.errin,
        'errOut': net_state.errout,
        'dropIn': net_state.dropin,
        'dropOut': net_state.dropout,
    }
