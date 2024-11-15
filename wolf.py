import math

class Wolf:
    def __init__(self, wolf_movement_distance):
        self.__position = {"pos_x": 0, "pos_y": 0}
        self.__movement_distance = wolf_movement_distance

    # def calc_distance(self, list_of_sheep):
    #     distances = []
    #     for list_of_sheep in list_of_sheep:
    #         distance = math.sqrt(dx ** 2 + dy ** 2)
    #         distances.append(distance)
    #     index_of_sheep = distances.index(min(distances))

    def move_towards(self, target_x, target_y):
        dx = target_x - self.__position["pos_x"]
        dy = target_y - self.__position["pos_y"]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance <= self.__movement_distance:
            self.__position["pos_x"] = target_x
            self.__position["pos_y"] = target_y
            return True

        dx /= distance
        dy /= distance

        self.__position["pos_x"] += dx
        self.__position["pos_y"] += dy

        return False

    def get_position(self):
        return self.__position




    def __str__(self):
        return f"Position: X={self.__position['pos_x']}, Y={self.__position['pos_y']}"
