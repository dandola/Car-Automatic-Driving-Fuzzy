from .fuzzy_variable import lightstatus_green
from .fuzzy_variable import lightstatus_less_green
from .fuzzy_variable import lightstatus_less_red
from .fuzzy_variable import lightstatus_red
from .fuzzy_variable import lightstatus_yellow

from .fuzzy_variable import distance_near
from .fuzzy_variable import distance_far
from .fuzzy_variable import distance_normal

from .fuzzy_variable import deviation_more_left
from .fuzzy_variable import deviation_left
from .fuzzy_variable import deviation_middle
from .fuzzy_variable import deviation_right
from .fuzzy_variable import deviation_more_right


def fuzzy_deviation(deviation):
    resut = {}

    value, weight = deviation_more_right(deviation)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        resut['farright'] = data

    value, weight = deviation_right(deviation)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        resut['right'] = data

    value, weight = deviation_middle(deviation)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        resut['middle'] = data

    value, weight = deviation_left(deviation)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        resut['left'] = data

    value, weight = deviation_more_left(deviation)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        resut['farleft'] = data

    return resut

def fuzzy_lightstatus(time_normalize):
    result = {}

    value, weight = lightstatus_green(time_normalize)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        result['green'] = data

    value, weight = lightstatus_less_green(time_normalize)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        result['less_green'] = data

    value, weight = lightstatus_yellow(time_normalize)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        result['yellow'] = data

    value, weight = lightstatus_less_red(time_normalize)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        result['less_red'] = data

    value, weight = lightstatus_red(time_normalize)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        result['red'] = data

    return result

def fuzzy_distance(distance):
    reslut = {}

    value, weight = distance_near(distance)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        reslut['near'] = data

    value, weight = distance_normal(distance)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        reslut['normal'] = data

    value, weight = distance_far(distance)
    if value != 0:
        data = {}
        data['value'] = value
        data['weight'] = weight
        reslut['far'] = data

    return reslut








