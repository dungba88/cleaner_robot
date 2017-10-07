class DFSSweeper(object):
    def __init__(self, robot):
        self.observed_map = {}
        self.robot = robot
        self.loggable = True

    def sweep(self):
        self.move({'x': 0, 'y': 0}, 0)

    def move(self, cur, dir):
        self.observed_map[str(cur['x'])+'_'+str(cur['y'])] = 1
        straight = self.next_straight(cur, dir)
        if not self.visited(straight) and self.robot.move():
            self.move(straight, dir)

        turn_taken = 0

        right = self.next_right(cur, dir)
        if not self.visited(right):
            self.robot.turn_right()
            turn_taken += 1
            if self.robot.move():
                self.move(right, (dir + 1) % 4)

        down = self.next_down(cur, dir)
        if not self.visited(down):
            for _ in range(2 - turn_taken):
                self.robot.turn_right()
                turn_taken += 1
            if self.robot.move():
                self.move(down, (dir + 2) % 4)

        left = self.next_left(cur, dir)
        if not self.visited(left):
            for _ in range(3 - turn_taken):
                self.robot.turn_right()
                turn_taken += 1
            if self.robot.move():
                self.move(left, (dir + 3) % 4)

        left_turns = turn_taken - 2
        if left_turns < 0:
            for _ in range(abs(left_turns)):
                self.robot.turn_right()
        else:
            for _ in range(left_turns):
                self.robot.turn_left()
        self.robot.move()
        self.robot.turn_left().turn_left()

    def next_straight(self, cur, dir):
        return {'x': cur['x'] - ((dir + 1) % 2) * (dir - 1), 'y': cur['y'] - (dir % 2) * (dir - 2)}

    def next_right(self, cur, dir):
        return {'x': cur['x'] + (dir % 2) * (dir - 2), 'y': cur['y'] - ((dir + 1) % 2) * (dir - 1)}

    def next_left(self, cur, dir):
        return {'x': cur['x'] - (dir % 2) * (dir - 2), 'y': cur['y'] + ((dir + 1) % 2) * (dir - 1)}

    def next_down(self, cur, dir):
        return {'x': cur['x'] + ((dir + 1) % 2) * (dir - 1), 'y': cur['y'] + (dir % 2) * (dir - 2)}

    def visited(self, node):
        return (str(node['x'])+'_'+str(node['y'])) in self.observed_map
