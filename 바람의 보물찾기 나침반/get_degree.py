from find_location import loc
from collection import find_closest_collection
import math

# 내 위치와 가장 가까운 재료의 방위와 각도를 계산하는 함수
def get_angle(my_position, closest_collection):
    # 내 위치와 가장 가까운 재료의 좌표 차이를 구합니다.
    delta_x = closest_collection[0] - my_position[0]
    delta_y = closest_collection[1] - my_position[1]
    
    # 각도를 계산합니다.
    angle = math.degrees(math.atan2(delta_y, delta_x))
    if angle < 0:
        angle += 360

    return angle - 90

def get_deg():
    my_position = loc()
    # print(my_position)
    cloest_collection, distance = find_closest_collection(my_position)
    # print(cloest_collection)
    if cloest_collection != None:
        angle = get_angle(my_position, cloest_collection)
        return ((my_position[0], my_position[1]), (cloest_collection[0], cloest_collection[1]), (my_position[0] - cloest_collection[0], my_position[1] - cloest_collection[1]), distance, angle, my_position[2])
    
    return ((my_position[0], my_position[1]), None, None, None, None, None)

if __name__ == "__main__":
    print(get_deg())