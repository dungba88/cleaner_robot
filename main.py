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
    no_rows = 10
    no_cols = 9
    no_obs = 10
    no_matrix = 1

    total_elapsed_bfs = 0
    total_steps_bfs = 0
    total_turns_bfs = 0

    total_elapsed_dfs = 0
    total_steps_dfs = 0
    total_turns_dfs = 0

    import time
    for i in range(no_matrix):
        matrix, start_position = random_matrix(no_rows, no_cols, no_obs)
        start_direction = random.randint(0, 3)

        # run with dfs
        robot = Robot(matrix, start_position, start_direction)
        # robot.log()
        sweeper = DFSSweeper(robot)
        sweeper.loggable = False
        robot.loggable = True

        start = time.time()
        sweeper.sweep()
        elapsed = time.time() - start

        total_elapsed_dfs += elapsed
        total_steps_dfs += robot.move_count
        total_turns_dfs += robot.turn_count

        print('steps taken by dfs: %d, turns taken: %d, time taken: %.2fms'
              % (robot.move_count, robot.turn_count, elapsed * 1000))

        # run with bfs
        robot = Robot(matrix, start_position, start_direction)
        sweeper = Sweeper(robot)
        sweeper.loggable = False
        robot.loggable = True

        # start = time.time()
        # sweeper.sweep()
        # elapsed = time.time() - start

        total_elapsed_bfs += elapsed
        total_steps_bfs += robot.move_count
        total_turns_bfs += robot.turn_count

        print('steps taken by planned bfs: %d, turns taken: %d, time taken: %.2fms'
              % (robot.move_count, robot.turn_count, elapsed * 1000))

        # sweeper.print_map()
        # robot.log()

    print('DFS: average steps taken: %d, turns taken: %d, time taken: %.2fms'
         % (int(total_steps_dfs / no_matrix), int(total_turns_dfs / no_matrix), total_elapsed_dfs * 1000 / no_matrix))

    print('Planned BFS: average steps taken: %d, turns taken: %d, time taken: %.2fms'
         % (int(total_steps_bfs / no_matrix), int(total_turns_bfs / no_matrix), total_elapsed_bfs * 1000 / no_matrix))

if __name__ == '__main__':
    main()
