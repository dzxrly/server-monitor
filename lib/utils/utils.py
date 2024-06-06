from typing import Union


def unit_convert(
        input_value: Union[float, int],
        input_unit: str,
        output_unit: str,
) -> float:
    """
    存储单位转换，以1024为基数
    :param input_value: 输入值
    :param input_unit: 输入单位，可选值为B, KB, MB, GB, TB
    :param output_unit: 输出单位，可选值为B, KB, MB, GB, TB
    :return: float
    """

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


def temperature_convert(
        input_value: float,
        input_unit: str,
        output_unit: str,
) -> float:
    """
    温度单位转换，以摄氏度为基数
    :param input_value: 输入值
    :param input_unit: 输入单位，可选值为C, F
    :param output_unit: 输出单位，可选值为C, F
    :return: float
    """

    assert input_unit in ['C', 'F'], \
        '[ERROR] temperature_convert: input_unit must be one of C, F'
    assert output_unit in ['C', 'F'], \
        '[ERROR] temperature_convert: output_unit must be one of C, F'

    if input_unit == 'F':
        input_value = (input_value - 32) / 1.8

    if output_unit == 'F':
        return input_value * 1.8 + 32

    return input_value


def flask_request_arg_bool(
        arg: str,
) -> bool:
    """
    Flask请求参数转换为bool类型
    :param arg: 请求参数
    :return: bool
    """
    return arg.lower() == 'true'
