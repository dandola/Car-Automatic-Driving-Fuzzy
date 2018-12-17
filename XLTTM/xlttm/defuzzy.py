from .fuzzy_variable import speed_medium
from .fuzzy_variable import speed_slower
from .fuzzy_variable import speed_slow
from .fuzzy_variable import speed_stop

from .fuzzy_variable import direction_hard_left
from .fuzzy_variable import direction_left
from .fuzzy_variable import direction_right
from .fuzzy_variable import direction_hard_right
from .fuzzy_variable import direction_middle

def defuzzy_steering(name_rule, value):
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

def defuzzy_speed(name_rule, value):
    if name_rule == 'stop':
        return speed_stop(value)
    if name_rule == 'slow':
        return speed_slow(value)
    if name_rule == 'slower':
        return speed_slower(value)
    if name_rule == 'medium':
        return speed_medium(value)
