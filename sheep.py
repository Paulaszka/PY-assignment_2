import random


class Sheep:
    def __init__(self, initial_position_limit, sheep_movement_distance):
        self.__position = {"pos_x": random.uniform(-initial_position_limit, initial_position_limit),
                           "pos_y": random.uniform(-initial_position_limit, initial_position_limit)}
        self.__movement_distance = sheep_movement_distance
        self.__eaten = False

    def move(self):
        directions = ["north", "south", "east", "west"]
        direction = random.choice(directions)
        match direction:
            case "north":
                self.__position["pos_y"] += self.__movement_distance
            case "south":
                self.__position["pos_y"] -= self.__movement_distance
            case "east":
                self.__position["pos_x"] += self.__movement_distance
            case "west":
                self.__position["pos_x"] -= self.__movement_distance

    def get_position(self):
        return self.__position

    def eat(self):
        self.__eaten = True
        self.__position["pos_x"] = None
        self.__position["pos_y"] = None

    def is_eaten(self):
        return self.__eaten
