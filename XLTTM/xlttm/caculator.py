import numpy as np
import io
from .args import rule_2
from .args import rule_1
from .args import rule_3
from .args import rule_4
from .args import rule_5
from .args import rule_6

from .fuzzy import fuzzy_deviation
from .fuzzy import fuzzy_distance
from .fuzzy import fuzzy_lightstatus

from .defuzzy import defuzzy_speed
from .defuzzy import defuzzy_steering

def cal_speed(lightstatus, distance, deviation):
    results = []
    rules = []
    with io.open(rule_2, 'r', encoding='utf-8') as f:
        for line in f:
            rule = line.split(',')
            rule[-1] = rule[-1].strip()
            rules.append(rule)

    result_deviation = fuzzy_deviation(deviation)
    result_distance = fuzzy_distance(distance)
    result_lightstatus = fuzzy_lightstatus(lightstatus)

    for rule in rules:
        value = [1, 1, 1]
        weight = [1, 1, 1]
        if rule[0] not in result_lightstatus.keys() and rule[0] != '_':
            continue
        if rule[1] not in result_distance.keys() and rule[1] != '_':
            continue
        if rule[2] not in result_deviation.keys() and rule[2] != '_':
            continue

        if rule[0] != '_':
            value[0] = result_lightstatus[rule[0]]['value']
            weight[0] = result_lightstatus[rule[0]]['weight']

        if rule[1] != '_':
            value[1] = result_distance[rule[1]]['value']
            weight[1] = result_distance[rule[1]]['weight']

        if rule[2] != '_':
            value[2] = result_deviation[rule[2]]['value']
            weight[2] = result_deviation[rule[2]]['weight']

        value = np.min(value)
        value = defuzzy_speed(rule[3], value)
        weight = weight[0] * weight[1] * weight[2]

        results.append((value, weight))

    total_value = 0
    total_weight = 0
    for result in results:
        total_value += result[0] * result[1]
        total_weight += result[1]

    if total_weight == 0:
        return None
    results = total_value / total_weight

    return results


def cal_steering(deviation):
    results = []
    rules = []

    with io.open(rule_1, 'r', encoding='utf-8') as f:
        for line in f:
            rule = line.split(',')
            rule[-1] = rule[-1].strip()
            rules.append(rule)

    result_deviation = fuzzy_deviation(deviation)

    for rule in rules:
        value =[1]
        weight = [1]

        if rule[0] not in result_deviation.keys() and rule[0] != '_':
            continue

        if rule[0] != '_':
            value[0] = result_deviation[rule[0]]['value']
            weight[0] = result_deviation[rule[0]]['weight']

        value = np.min(value)
        value = defuzzy_steering(rule[1], value)
        weight = weight[0]

        results.append((value, weight))

    total_value = 0
    total_weight = 0
    for result in results:
        total_value += result[0] * result[1]
        total_weight += result[1]

    if total_weight == 0:
        return None
    results = total_value / total_weight

    return results

def cal_steering_left(deviation, distance_stone=200):
    results = []
    rules = []

    with io.open(rule_3, 'r', encoding='utf-8') as f:
        for line in f:
            rule = line.split(',')
            rule[-1] = rule[-1].strip()
            rules.append(rule)

    result_deviation = fuzzy_deviation(deviation)
    result_distance_stone = fuzzy_distance(distance_stone)

    for rule in rules:
        value =[1, 1]
        weight = [1, 1]

        if rule[0] not in result_distance_stone.keys() and rule[0] != '_':
            continue

        if rule[1] not in result_deviation.keys() and rule[0] != '_':
            continue

        if rule[0] != '_':
            value[0] = result_distance_stone[rule[0]]['value']
            weight[0] = result_distance_stone[rule[0]]['weight']

        if rule[1] != '_':
            value[1] = result_deviation[rule[1]]['value']
            weight[1] = result_deviation[rule[1]]['weight']

        value = np.min(value)
        value = defuzzy_steering(rule[2], value)
        weight = weight[0] * weight[1]

        results.append((value, weight))

    total_value = 0
    total_weight = 0
    for result in results:
        total_value += result[0] * result[1]
        total_weight += result[1]

    if total_weight == 0:
        return None
    results = total_value / total_weight

    return results

def cal_steering_right(deviation, distance_stone=200):
    results = []
    rules = []

    with io.open(rule_4, 'r', encoding='utf-8') as f:
        for line in f:
            rule = line.split(',')
            rule[-1] = rule[-1].strip()
            rules.append(rule)

    result_deviation = fuzzy_deviation(deviation)
    result_distance_stone = fuzzy_distance(distance_stone)

    for rule in rules:
        value =[1, 1]
        weight = [1, 1]

        if rule[0] not in result_distance_stone.keys() and rule[0] != '_':
            continue

        if rule[1] not in result_deviation.keys() and rule[0] != '_':
            continue

        if rule[0] != '_':
            value[0] = result_distance_stone[rule[0]]['value']
            weight[0] = result_distance_stone[rule[0]]['weight']

        if rule[1] != '_':
            value[1] = result_deviation[rule[1]]['value']
            weight[1] = result_deviation[rule[1]]['weight']

        value = np.min(value)
        value = defuzzy_steering(rule[2], value)
        weight = weight[0] * weight[1]

        results.append((value, weight))

    total_value = 0
    total_weight = 0
    for result in results:
        total_value += result[0] * result[1]
        total_weight += result[1]

    if total_weight == 0:
        return None
    results = total_value / total_weight

    return results


def cal_speed_stone_left( deviation, distance_stone=200, distance_two_stone=200):
    results = []
    rules = []

    with io.open(rule_5, 'r', encoding='utf-8') as f:
        for line in f:
            rule = line.split(',')
            rule[-1] = rule[-1].strip()
            rules.append(rule)

    result_distance_stone = fuzzy_distance(distance_stone)
    result_distance_two_stone = fuzzy_distance(distance_two_stone)
    result_deviation = fuzzy_deviation(deviation)

    for rule in rules:
        value = [1, 1, 1]
        weight = [1, 1, 1]
        if rule[0] not in result_distance_stone.keys() and rule[0] != '_':
            continue
        if rule[1] not in result_distance_two_stone.keys() and rule[1] != '_':
            continue
        if rule[2] not in result_deviation.keys() and rule[2] != '_':
            continue

        if rule[0] != '_':
            value[0] = result_distance_stone[rule[0]]['value']
            weight[0] = result_distance_stone[rule[0]]['weight']

        if rule[1] != '_':
            value[1] = result_distance_two_stone[rule[1]]['value']
            weight[1] = result_distance_two_stone[rule[1]]['weight']

        if rule[2] != '_':
            value[2] = result_deviation[rule[2]]['value']
            weight[2] = result_deviation[rule[2]]['weight']

        value = np.min(value)
        value = defuzzy_speed(rule[3], value)
        weight = weight[0] * weight[1] * weight[2]

        results.append((value, weight))

    total_value = 0
    total_weight = 0
    for result in results:
        total_value += result[0] * result[1]
        total_weight += result[1]

    if total_weight == 0:
        return None
    results = total_value / total_weight

    return results

def cal_speed_stone_right(deviation, distance_stone=200, distance_two_stone=200):
    results = []
    rules = []

    with io.open(rule_6, 'r', encoding='utf-8') as f:
        for line in f:
            rule = line.split(',')
            rule[-1] = rule[-1].strip()
            rules.append(rule)

    result_distance_stone = fuzzy_distance(distance_stone)
    result_distance_two_stone = fuzzy_distance(distance_two_stone)
    result_deviation = fuzzy_deviation(deviation)

    for rule in rules:
        value = [1, 1, 1]
        weight = [1, 1, 1]
        if rule[0] not in result_distance_stone.keys() and rule[0] != '_':
            continue
        if rule[1] not in result_distance_two_stone.keys() and rule[1] != '_':
            continue
        if rule[2] not in result_deviation.keys() and rule[2] != '_':
            continue

        if rule[0] != '_':
            value[0] = result_distance_stone[rule[0]]['value']
            weight[0] = result_distance_stone[rule[0]]['weight']

        if rule[1] != '_':
            value[1] = result_distance_two_stone[rule[1]]['value']
            weight[1] = result_distance_two_stone[rule[1]]['weight']

        if rule[2] != '_':
            value[2] = result_deviation[rule[2]]['value']
            weight[2] = result_deviation[rule[2]]['weight']

        value = np.min(value)
        value = defuzzy_speed(rule[3], value)
        weight = weight[0] * weight[1] * weight[2]

        results.append((value, weight))

    total_value = 0
    total_weight = 0
    for result in results:
        total_value += result[0] * result[1]
        total_weight += result[1]

    if total_weight == 0:
        return None
    results = total_value / total_weight

    return results

