class Wolf:
    def __init__(self, wolf_movement_distance):
        self.__position = {"pos_x": 0, "pos_y": 0}
        self.__movement_distance = wolf_movement_distance

    def move_towards(self, target_x, target_y):
        dx = target_x - self.__position["pos_x"]
        dy = target_y - self.__position["pos_y"]

        distance = dx ** 2 + dy ** 2

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

    def print_position(self):
        print("Wolf is on position: ({:.3f}, {:.3f})".format(self.__position["pos_x"], self.__position["pos_y"]))

