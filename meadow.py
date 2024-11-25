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
        self.__num_of_alive_sheep = len(self.__sheep_list)

    def __get_nearest_sheep(self):
        wolf_position = self.__wolf.get_position()
        distances = []
        for sheep_instance in self.__sheep_list:
            if sheep_instance is None:
                distances.append(float('inf'))
            else:
                sheep_position = sheep_instance.get_position()
                distance = ((sheep_position["pos_x"] - wolf_position["pos_x"]) ** 2
                            + (sheep_position["pos_y"] - wolf_position["pos_y"]) ** 2)
                distances.append(distance)
        index = distances.index(min(distances))
        return self.__sheep_list[index], index

    def __next_round(self):
        for sheep_instance in self.__sheep_list:
            if sheep_instance is not None:
                sheep_instance.move()
        nearest_sheep, sheep_index = self.__get_nearest_sheep()
        nearest_sheep_position = nearest_sheep.get_position()
        print(f"Wolf is chasing sheep number {sheep_index + 1}!")
        if self.__wolf.move_towards(nearest_sheep_position["pos_x"], nearest_sheep_position["pos_y"]):
            self.__sheep_list[sheep_index] = None
            self.__num_of_alive_sheep = self.__num_of_alive_sheep - 1
            print(f"Sheep number {sheep_index + 1} has been eaten!")
        if all(sheep_inst is None for sheep_inst in self.__sheep_list):
            return True
        return False

    def start(self):
        for i in range(self.__num_of_rounds):
            print(f"\nRound number {i + 1}")
            self.__wolf.print_position()
            if len(self.__sheep_list) == 1:
                print(f"There is {self.__num_of_alive_sheep} sheep alive.")
            else:
                print(f"There are {self.__num_of_alive_sheep} sheep alive.")

            if self.__next_round():
                print("All sheep eaten!")
                break


if __name__ == '__main__':
    meadow = Meadow(50, 15, 10, 0.5, 1)
    meadow.start()
