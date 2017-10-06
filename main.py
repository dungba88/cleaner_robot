from robot import Robot
from sweeper import Sweeper

def main():
    matrix = [
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0]
    ]
    start_position = {'x': 0, 'y': 1}
    start_direction = 1

    robot = Robot(matrix, start_position, start_direction)
    sweeper = Sweeper(robot)
    sweeper.loggable = False
    robot.loggable = False

    import time
    start = time.time()
    steps = sweeper.sweep()
    elapsed = time.time() - start

    print('steps taken: %d, time taken: %.2fms' % (steps, elapsed * 1000))
    sweeper.print_map()

if __name__ == '__main__':
    main()
