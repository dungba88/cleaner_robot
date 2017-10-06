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
    steps = sweeper.sweep()

    print('average steps: %d' % steps)
    sweeper.print_map()

if __name__ == '__main__':
    main()
