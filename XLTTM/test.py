from xlttm import cal_steering, cal_speed
from xlttm import cal_speed_stone_left, cal_speed_stone_right
from xlttm import cal_steering_right, cal_steering_left
import numpy as np


# print(cal_steering(0.9))
# print(distance_normal(12))
# print(cal_speed(0.85, 175, 0.3))
# print(fuzzy_deviation(0.1))
# print(deviation_more_left(0.1))
# print(cal_steering_left(15, 0.75))
# print(cal_speed_stone_left(15, 13, 0.4))
# print()

def test_steering():
    values = np.linspace(0, 1, 11)
    with open('steering_1.txt', 'w') as f:
        for value in values:
            result = cal_steering(value)
            content = str(value) +','+ str(result)+'\n'
            f.write(content)

def test_speed():
    values = np.linspace(0, 1, 11)
    distance_values = np.linspace(0, 200, 21)
    with open('speed_1.txt', 'w') as f:
        for light_status in values:
            for distance in distance_values:
                for deviation in values:
                    result = cal_speed(light_status, distance, deviation)
                    content = str(light_status) + ','+ str(distance) + ',' \
                              + str(deviation) + ','+ str(result) +'\n'
                    f.write(content)

def test_stone_steering():
    values = np.linspace(0, 1, 11)
    distance_values = np.linspace(0, 200, 21)
    with open('steering_2.txt', 'w') as f:
        for distance in distance_values:
            for value in values:
                result = cal_steering_right(distance, value)
                content = str(distance) +','+str(value)+','+str(result)+ '\n'
                f.write(content)

def test_stone_speed():
    values = np.linspace(0, 1, 11)
    distance_values = np.linspace(0, 200, 21)
    with open('speed_2.txt', 'w') as f:
        for distance_stone in distance_values:
            for distance_2stone in distance_values:
                for value in values:
                    result = cal_speed_stone_left(distance_stone, distance_2stone, value)
                    content = str(distance_stone) + ','+ str(distance_2stone) +\
                              ',' + str(value) + ',' + str(result)+ '\n'
                    f.write(content)

if __name__ == '__main__':
    # test_steering()
    # test_speed()
    # test_stone_steering()
    # test_stone_speed()
    print(cal_steering_right(0.5, 55.22))



#
# 1) cal_steering(deviation) -> return deviation1
# 2) cal_speed(lightstatus, distance, deviation) --> return vel1
#
#
# 3) cal_steering_left(deviation, distance_stone=200) --> return deviation2
# 4) cal_speed_stone_left( deviation, distance_stone=200, distance_two_stone=200) --> return vel2
#
#
# 5) cal_steering_right(deviation, distance_stone=200) --> return deviation2
# 6) cal_speed_stone_right(deviation, distance_stone=200, distance_two_stone=200) --> return vel2

# van toc tu 0 --> 100
#
# running:
# 1) --> return deviation1
# 2) --> return vel1
# if left_stone:
#     3) --> return deviation2
#     4) -->return vel2
# else:
#     5) --> return deviation2
#     6) --> return vel2
#
# if vel1==None:
#     if vel2 == None:
#         vt= 1
#     else: vt = vel2
# else:
#     if vel2==None:
#         vt= vel1
#     else:
#         vel = min(vel1, vel2)



# if deviation1 == None:
#     if deviation2==None:
#         deviation  = goc ban dau
#     else:
#         deviation  = deviation2
# else:
#     if deviation2 == None:
#         deviation = deviation1
#     else:
#         if(deviation1 < 0.5 and deviation2 < 0.5):
#             deviation  = min(deviation1, deviation2)
#         elif deviation1 > 0.5 and deviation2 > 0.5:
#             deviation  = max(deviation1,deviation2)
#         elif deviation2 == 0.5:
#             deviation  = deviation1
#         else:
#             deviation  = deviation2
#
#
#
