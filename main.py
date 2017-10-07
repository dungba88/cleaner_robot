import random

from robot import Robot
from sweeper import Sweeper
from dfs_sweeper import DFSSweeper

def random_matrix(no_rows, no_cols, no_obs):
    arr = []
    for i in range(no_rows * no_cols):
        if i < no_obs:
            arr.append(1)
        else:
            arr.append(0)

    random.shuffle(arr)

    start_position = {'x': 0, 'y': 0}
    rand_pos = random.randint(0, no_rows * no_cols - no_obs - 1)

    matrix = []
    count = 0
    for i in range(no_rows):
        row = []
        for j in range(no_cols):
            row.append(arr[i * no_cols + j])
            if arr[j] == 0:
                if count == rand_pos:
                    start_position = {'x': j, 'y': i}
                count += 1
        matrix.append(row)
    return matrix, start_position

def main():
    no_rows = 4
    no_cols = 3
    no_obs = 2
    no_matrix = 1

    total_elapsed = 0
    total_steps = 0
    total_turns = 0

    for i in range(no_matrix):
        matrix, start_position = random_matrix(no_rows, no_cols, no_obs)
        start_direction = random.randint(0, 3)
        robot = Robot(matrix, start_position, start_direction)
        sweeper = DFSSweeper(robot)
        sweeper.loggable = False

        robot.log()

        import time

        start = time.time()
        sweeper.sweep()
        elapsed = time.time() - start

        total_elapsed += elapsed
        total_steps += robot.move_count
        total_turns += robot.turn_count

        print('steps taken: %d, turns taken: %d, time taken: %.2fms'
              % (robot.move_count, robot.turn_count, elapsed * 1000))

        # sweeper.print_map()
        robot.log()

    print('average steps taken: %d, turns taken: %d, time taken: %.2fms'
         % (int(total_steps / no_matrix), int(total_turns / no_matrix), total_elapsed * 1000 / no_matrix))

if __name__ == '__main__':
    main()
