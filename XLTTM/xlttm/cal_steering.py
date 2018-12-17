from .fuzzy_variable import deviation_more_left, deviation_left
from .fuzzy_variable import deviation_middle
from .fuzzy_variable import deviation_right, deviation_more_right

from .fuzzy_variable import direction_hard_left, direction_left
from .fuzzy_variable import direction_middle
from .fuzzy_variable import direction_right, direction_hard_right

import numpy as np

rule_path = './xlttm/deviation2steering.txt'

def load_rule():
    all_rules = {}
    with open(rule_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = line.split(',')
            data[-1] = data[-1].strip()
            all_rules[data[0]] = data[1]
    return all_rules

def defuzzy(name_rule, value):
    if name_rule == 'hardleft':
        return direction_hard_left(value)
    if name_rule == 'left':
        return  direction_left(value)
    if name_rule == 'middle':
        return direction_middle(value)
    if name_rule == 'right':
        return direction_right(value)
    if name_rule == 'hardright':
        return direction_hard_right(value)

def cal_steering(deviation):
    all_rule = load_rule()
    steering_result = []

    tmp_value, tmp_weight = deviation_more_left(deviation)
    if tmp_value != 0:
        tmp_value = defuzzy(all_rule['farleft'], deviation)
        steering_result.append([tmp_value, tmp_weight])

    tmp_value, tmp_weight = deviation_left(deviation)
    if tmp_value != 0:
        tmp_value = defuzzy(all_rule['left'], deviation)
        steering_result.append([tmp_value, tmp_weight])

    tmp_value, tmp_weight = deviation_middle(deviation)
    if tmp_value != 0:
        tmp_value =  defuzzy(all_rule['middle'], deviation)
        steering_result.append([tmp_value, tmp_weight])

    tmp_value, tmp_weight = deviation_right(deviation)
    if tmp_value != 0:
        tmp_value = defuzzy(all_rule['right'], deviation)
        steering_result.append([tmp_value, tmp_weight])

    tmp_value, tmp_weight = deviation_more_right(deviation)
    if tmp_value != 0:
        tmp_value = defuzzy(all_rule['farright'], deviation)
        steering_result.append([tmp_value, tmp_weight])

    tu_so = 0
    mau_so = 0
    for value in steering_result:
        tu_so = tu_so + value[0] * value[1]
        mau_so = mau_so + value[1]

    steering_result = tu_so / mau_so

    return steering_result
