import numpy as np

def deviation_more_left(deviation):

    if deviation < 0.25:
        return 1, 1

    if 0.25 <= deviation <= 0.4:
        value = -6.67 * deviation + 2.67
        w = np.abs(0.4 - deviation) / (0.4 - 0.25)
        return value, w

    if deviation > 0.4:
        return 0, 0

def deviation_left(deviation):

    if deviation < 0.25:
        return 0, 0

    if 0.25 <= deviation <= 0.4:
        value = 6.67 * deviation - 1.67
        w = np.abs(0.25 - deviation) / (0.4 - 0.25)
        return value, w

    if 0.4 <= deviation <= 0.5:
        value = -10 * deviation + 5
        w = np.abs(0.5 - deviation) / (0.5 - 0.4)
        return value, w

    if deviation > 0.5:
        return 0, 0

def deviation_middle(deviation):

    if deviation < 0.4:
        return 0, 0

    if 0.4 <= deviation <= 0.5:
        value = 10* deviation - 4
        w = np.abs(0.4 - deviation) / (0.5 - 0.4)
        return value, w

    if 0.5 <= deviation <= 0.6:
        value = -10 * deviation +6
        w = np.abs(0.6 - deviation) / (0.6 - 0.5)
        return value, w

    if deviation > 0.6:
        return 0, 0

def deviation_right(deviation):

    if deviation < 0.5:
        return 0, 0

    if 0.5 <= deviation <= 0.6:
        value = 10 * deviation - 5
        w = np.abs(0.5 - deviation) / (0.6 -0.5)
        return value, w

    if 0.6 <= deviation <= 0.75:
        value = -6.67*deviation + 5
        w = np.abs(0.75- deviation) / (0.75 - 0.6)
        return value, w

    if deviation > 0.75:
        return 0, 0

def deviation_more_right(deviation):

    if deviation < 0.6:
        return 0, 0

    if 0.6 <= deviation <= 0.75:
        value = 6.67 * deviation - 4
        w = np.abs(0.6 - deviation) / (0.75 - 0.6)
        return value, w

    if deviation > 0.75:
        return 1, 1

def lightstatus_green(time_normalize):

    if time_normalize < 0.25:
        return 1, 1

    if 0.25 <= time_normalize <= 0.4:
        value = -6.67 * time_normalize + 2.67
        w = np.abs(0.4 - time_normalize) / (0.4 - 0.25)
        return value, w

    if time_normalize > 0.4:
        return 0, 0

def lightstatus_less_green(time_normalize):

    if time_normalize < 0.33:
        return 0, 0

    if 0.33 <= time_normalize <= 0.417:
        value = 11.5 * time_normalize - 3.795
        w = np.abs(0.33 - time_normalize) / (0.417 - 0.33)
        return value, w

    if 0.417 <= time_normalize <= 0.542:
        value = -8 * time_normalize + 4.336
        w = np.abs(0.542 - time_normalize) / (0.542 - 0.417)
        return value, w

    if time_normalize > 0.542:
        return 0, 0

def lightstatus_yellow(time_normalize):

    if time_normalize < 0.458:
        return 0, 0

    if 0.458 <= time_normalize <= 0.542:
        value = 11.9 * time_normalize - 5.45
        w = np.abs(0.458 - time_normalize) / (0.542 - 0.458)
        return value, w

    if 0.542 <= time_normalize <= 0.708:
        value = -6 * time_normalize + 4.25
        w = np.abs(0.708 - time_normalize) / (0.708 - 0.542)
        return value, w

    if time_normalize > 0.708:
        return 0, 0

def lightstatus_red(time_normalize):

    if time_normalize < 0.625:
        return 0, 0

    if 0.625 <= time_normalize <= 0.67:
        value = 22.22 * time_normalize - 13.89
        w = np.abs(0.625 - time_normalize) / (0.625 - 0.67)
        return value, w

    if 0.67 <= time_normalize <= 0.83:
        return 1, 1

    if 0.83 <= time_normalize <= 0.9:
        value = -14.29 * time_normalize + 12.86
        w = np.abs(0.9 - time_normalize) / (0.9 - 0.83)
        return value, w

    if time_normalize > 0.9:
        return 0, 0

def lightstatus_less_red(time_normalize):

    if time_normalize < 0.83:
        return 0, 0

    if 0.83 <= time_normalize <= 0.917:
        value = 11.49 * time_normalize - 9.54
        w = np.abs(0.83 - time_normalize) / (0.917 - 0.83)
        return value, w

    if time_normalize > 0.917:
        return 1, 1

def distance_near(distance):

    if distance < 10:
        return 1, 1

    if 10 <= distance <= 40:
        value = -0.033 * distance + 1.33
        w = np.abs(40 - distance) / (40 - 10)
        return value, w

    if distance > 40:
        return 0, 0

def distance_normal(distance):

    if distance < 10:
        return 0, 0

    if 10 <= distance <= 20:
        value = 0.1 * distance - 1
        w = np.abs(10 - distance) / (20 - 10)
        return value, w

    if 20 <= distance <= 50:
        return 1, 1

    if 50 <= distance <= 70:
        value = -0.05 * distance + 3.5
        w = np.abs(70 - distance)/(70-50)
        return value, w

    if distance > 70:
        return 0, 0

def distance_far(distance):

    if distance < 40:
        return 0, 0

    if 40 <= distance <= 70:
        value = 0.033 * distance - 1.33
        w = np.abs(40 - distance) / (70 - 40)
        return value, w

    if distance > 70:
        return 1, 1

# fuzzy -> variable

def direction_hard_left(value):

    x_left = 0
    x_right = (value - 2.67)/(-6.67)
    return (x_left + x_right) / 2

def direction_left(value):

    x_left = (value + 1.67) / 6.67
    x_right = (value - 5) / (-10)
    return (x_left + x_right) / 2

def direction_middle(value):

    x_left = (value + 4) / 10
    x_right = (value - 6) / (-10)
    return (x_left + x_right) / 2

def direction_right(value):

    x_left = (value + 5) / 10
    x_right = (value - 5)/ (-6.67)
    return (x_left + x_right) / 2


def direction_hard_right(value):

    x_left = (value + 4) / 6.67
    x_right = 1
    return (x_left + x_right) / 2

def speed_stop(value):

    x_left = 0
    x_right = (value - 1) / (-20)
    return (x_left + x_right) / 2

def speed_slower(value):

    x_left = (value + 0.11) / 4.44
    x_right = (value - 2) / (-4)
    return (x_left + x_right) / 2

def speed_slow(value):

    x_left = (value + 1) / 3.33
    x_right = (value - 4) / (-5)
    return (x_right + x_left) / 2

def speed_medium(value):

    x_left = (value + 3.5) / 5
    x_right = 1

    return (x_left + x_right) / 2