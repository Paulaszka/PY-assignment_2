import sheep
import wolf

class Meadow:
    def __init__(self, num_of_rounds, num_of_sheep,
                 init_position_limit, sheep_movement_dist_limit, wolf_movement_dist_limit):
        self.__num_of_rounds = num_of_rounds
        self.__sheep_list = []
        for i in range(num_of_sheep):
            self.__sheep_list.append(sheep.Sheep(init_position_limit, sheep_movement_dist_limit))
        self.__wolf = wolf.Wolf(wolf_movement_dist_limit)

    def __get_nearest_sheep(self):
        wolf_position = self.__wolf.get_position()
        distances = []
        for sheep_instance in self.__sheep_list:
            sheep_position = sheep_instance.get_position()
            distance = ((sheep_position["pos_x"] - wolf_position["pos_x"]) ** 2
                        + (sheep_position["pos_y"] - wolf_position["pos_y"]) ** 2)
            distances.append(distance)
        index = distances.index(min(distances))
        return self.__sheep_list[index]

    def __next_round(self):
        for sheep_instance in self.__sheep_list:
            sheep_instance.move()
        nearest_sheep = self.__get_nearest_sheep()
        nearest_sheep_position = nearest_sheep.get_position()
        if self.__wolf.move_towards(nearest_sheep_position["pos_x"], nearest_sheep_position["pos_y"]):
            self.__sheep_list.remove(nearest_sheep)
        if len(self.__sheep_list) == 0:
            return True
        return False

    def start(self):
        for i in range(self.__num_of_rounds):
            if self.__next_round():
                print(f"Round number {i + 1}")
                print("Sheep have been eaten")
                break
            else:
                print(f"Round number {i + 1}")


if __name__ == '__main__':
    meadow = Meadow(50, 15, 10,
                    0.5, 1)
    meadow.start()