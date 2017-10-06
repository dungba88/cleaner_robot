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
    robot.loggable = False
    steps = Sweeper(robot).sweep()

    print('average steps: %d' % steps)

if __name__ == '__main__':
    main()
