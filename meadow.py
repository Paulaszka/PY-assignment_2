import argparse
import csv
import json
import logging
import configparser
import sys

import sheep
import wolf


def setup_logging(log_level):
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    logging.basicConfig(
        filename='chase.log',
        level=log_levels.get(log_level, logging.INFO),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Wolf vs Sheep Simulation")
    parser.add_argument('-c', '--config', type=str, help="Path to the configuration file")
    parser.add_argument('-l', '--log', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set log level for logging")
    parser.add_argument('-r', '--rounds', type=int, help="Maximum number of rounds")
    parser.add_argument('-s', '--sheep', type=int, help="Number of sheep")
    parser.add_argument('-w', '--wait', action='store_true', help="Pause after each round until key press")

    return parser.parse_args()


# Load configuration file
def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    init_position_limit = float(config['Sheep'].get('InitPosLimit', 10.0))
    sheep_move_dist = float(config['Sheep'].get('MoveDist', 0.5))
    wolf_move_dist = float(config['Wolf'].get('MoveDist', 1.0))

    # Validate values
    if sheep_move_dist <= 0:
        raise ValueError("Sheep movement distance must be positive.")
    if wolf_move_dist <= 0:
        raise ValueError("Wolf movement distance must be positive.")

    return init_position_limit, sheep_move_dist, wolf_move_dist


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
        logging.debug(f'Wolf position is x: {round(pos["pos_x"], 3)}, y: {round(pos["pos_y"], 3)}')
        logging.debug(f'Wolf {action} sheep with index {sheep_index}')

    def __next_round(self, round_number):
        logging.info(f'Round {round_number + 1}')
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
            logging.info('All sheep have been eaten')
            print('All sheep have been eaten')
            return True

        logging.info(f'Number of sheep alive: {number_of_sheep_alive}')
        print(f'Number of sheep alive: {number_of_sheep_alive}')

        if args.wait:
            input("Press any key to continue to the next round...")

        return False

    def __to_json(self, round_number):
        sheep_json_list = []
        for sheep_instance in self.__sheep_list:
            sheep_json_list.append({
                "pos_x": sheep_instance.get_position()["pos_x"],
                "pos_y": sheep_instance.get_position()["pos_y"]
            })

        wolf_json = {
            "pos_x": self.__wolf.get_position()["pos_x"],
            "pos_y": self.__wolf.get_position()["pos_y"]
        }

        round_data = {
            "round_no": round_number + 1,
            "wolf_pos": wolf_json,
            "sheep_pos": sheep_json_list
        }

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
            try:
                with open(self.__csv_file_path, "r", newline="") as csv_file:
                    reader = csv.reader(csv_file)
                    existing_data = list(reader)
            except FileNotFoundError:
                existing_data = [['round_number', 'sheep_alive_count']]

            existing_data.append([round_number, sheep_count])

            with open(self.__csv_file_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(existing_data)
        except Exception as e:
            logging.error(f"An error occurred while saving CSV data: {e}")

    def start(self):
        for i in range(self.__num_of_rounds):
            if self.__next_round(i):
                break


if __name__ == '__main__':
    # Parse command-line arguments
    args = parse_args()

    # Handle logging
    if args.log:
        setup_logging(args.log)

    # Default values
    num_of_rounds = 50
    num_of_sheep = 15
    init_position_limit = 10.0
    sheep_move_dist = 0.5
    wolf_move_dist = 1.0

    # Load config if provided
    if args.config:
        try:
            init_position_limit, sheep_move_dist, wolf_move_dist = load_config(args.config)
        except Exception as e:
            logging.error(f"Error loading config file: {e}")
            sys.exit(1)

    if args.rounds:
        num_of_rounds = args.rounds
    if args.sheep:
        num_of_sheep = args.sheep

    meadow = Meadow(num_of_rounds, num_of_sheep, init_position_limit,
                    sheep_move_dist, wolf_move_dist, 'pos.json', 'alive.csv')
    meadow.start()
