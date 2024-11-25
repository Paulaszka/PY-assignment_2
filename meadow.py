import csv
import json

import sheep
import wolf


class Meadow:
    def __init__(self, num_of_rounds, num_of_sheep, init_position_limit,
                 sheep_movement_dist_limit, wolf_movement_dist_limit, json_file_path, csv_file_path):
        self.__num_of_rounds = num_of_rounds
        self.__sheep_list = [sheep.Sheep(init_position_limit, sheep_movement_dist_limit) for _ in range(num_of_sheep)]
        self.__wolf = wolf.Wolf(wolf_movement_dist_limit)
        self.__json_file_path = json_file_path
        self.__csv_file_path = csv_file_path

    def __get_nearest_sheep(self):
        wolf_position = self.__wolf.get_position()
        nearest_sheep = None
        min_distance = float("inf")

        for sheep_instance in self.__sheep_list:
            if not sheep_instance.is_eaten():
                sheep_position = sheep_instance.get_position()
                distance = ((sheep_position["pos_x"] - wolf_position["pos_x"]) ** 2
                            + (sheep_position["pos_y"] - wolf_position["pos_y"]) ** 2)
                if distance < min_distance:
                    nearest_sheep = sheep_instance
                    min_distance = distance
        return nearest_sheep

    def __log_wolf_action(self, action, sheep_index):
        pos = self.__wolf.get_position()
        print(f'Wolf position is x: {pos["pos_x"]:.3f}, y: {pos["pos_y"]:.3f}')
        print(f'Wolf {action} sheep with index {sheep_index}')

    def __next_round(self, round_number):
        print(f'Round {round_number + 1}')
        for sheep_instance in self.__sheep_list:
            if not sheep_instance.is_eaten():
                sheep_instance.move()

        nearest_sheep = self.__get_nearest_sheep()
        sheep_index = self.__sheep_list.index(nearest_sheep)
        nearest_sheep_position = nearest_sheep.get_position()

        if self.__wolf.move_towards(nearest_sheep_position["pos_x"], nearest_sheep_position["pos_y"]):
            nearest_sheep.eat()
            self.__log_wolf_action("has eaten", sheep_index)
        else:
            self.__log_wolf_action("is chasing", sheep_index)

        number_of_sheep_alive = 0
        for sheep_instance in self.__sheep_list:
            if not sheep_instance.is_eaten():
                number_of_sheep_alive += 1

        self.__to_json(round_number)
        self.__to_csv(round_number, number_of_sheep_alive)

        if number_of_sheep_alive == 0:
            print('All sheep have been eaten')
            return True

        print(f'Number of sheep alive: {number_of_sheep_alive}')
        return False

    def __to_json(self, round_number):
        sheep_json_list = []
        for sheep_instance in self.__sheep_list:
            sheep_json_list.append([
                sheep_instance.get_position()["pos_x"],
                sheep_instance.get_position()["pos_y"]
            ])

        wolf_json = [
            self.__wolf.get_position()["pos_x"],
            self.__wolf.get_position()["pos_y"]
        ]

        round_data = {
            "round_no": round_number + 1,
            "wolf_pos": wolf_json,
            "sheep_pos": sheep_json_list
        }

        if round_number == 0:
            data = []
        else:
            try:
                with open(self.__json_file_path, "r") as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError:
                        data = []
            except FileNotFoundError:
                data = []

        data.append(round_data)

        with open(self.__json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def __to_csv(self, round_number, sheep_count):
        try:
            if round_number == 0:
                existing_data = [['round_number', 'alive_sheep_count']]
            else:
                try:
                    with open(self.__csv_file_path, "r", newline="") as csv_file:
                        reader = csv.reader(csv_file)
                        existing_data = list(reader)
                except FileNotFoundError:
                    existing_data = [['round_number', 'sheep_alive_count']]

            existing_data.append([round_number + 1, sheep_count])

            with open(self.__csv_file_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(existing_data)
        except Exception as e:
            print(f"An error occurred: {e}")

    def start(self):
        for i in range(self.__num_of_rounds):
            if self.__next_round(i):
                break


if __name__ == '__main__':
    meadow = Meadow(50, 15, 10,
                    0.5, 1, 'pos.json', 'alive.csv')
    meadow.start()
