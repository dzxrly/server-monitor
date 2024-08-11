import platform

import psutil


def get_operating_system_info() -> dict:
    """
    获取操作系统的相关信息
    :return: 返回一个聚合信息的字典
    """
    architecture = platform.architecture()[0]
    uname = platform.uname()
    if psutil.WINDOWS:
        return {
            'os_name': '{} {} NT_Ver.{}'.format(uname.system, platform.win32_edition(), uname.version),
            'os_architecture': architecture,
            'os_sign': uname.system,
            'os_node': uname.node,
        }
    elif psutil.LINUX:
        _freedesktop_os_release = platform.freedesktop_os_release()
        return {
            'os_name': '{} {}'.format(_freedesktop_os_release['NAME'], _freedesktop_os_release['VERSION']),
            'os_architecture': architecture,
            'os_sign': uname.system,
            'os_node': uname.node,
        }
    else:
        raise NotImplementedError('Unsupported system')
