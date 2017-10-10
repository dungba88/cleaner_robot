from utils import sin, cos, bfs, print_observed_map

class Sweeper(object):
    def __init__(self, robot):
        self.current_direction = 0 # can be from 0 to 3, mapped to 0-270 degrees
        self.current_position = {'x': 0, 'y': 0}
        self.observed_map = {0: {0: 1}}
        self.robot = robot
        self.loggable = True
        self.spiral = True

    def sweep(self):
        while self.move():
            pass

    def move(self):
        self.log('looking for nearest unvisited position')
        target_path = self.find_nearest_unvisited_pos()
        if not target_path:
            self.log('cannot find nearest unvisited position, cleaned')
            return False
        self.log('found nearest unvisited position, moving there')
        self.move_with_path(target_path)
        return True

    def find_nearest_unvisited_pos(self):
        return bfs(self.current_position, self.current_direction, self.node_unvisited, self.adjacent_movable, self.spiral)

    def node_unvisited(self, node):
        map_node = self.get_node_from_map(node)
        return map_node is None

    def adjacent_movable(self, node):
        map_node = self.get_node_from_map(node)
        return map_node != -1

    def get_node_from_map(self, node):
        if not node['y'] in self.observed_map \
                or not node['x'] in self.observed_map[node['y']]:
            return None
        return self.observed_map[node['y']][node['x']]

    def move_with_path(self, target_path):
        for path in reversed(target_path):
            left_turns = path - self.current_direction
            if left_turns < 0:
                left_turns += 4
            # we don't need this, but in reality turning is costly
            # so instead of turning left 3 times, we'll turn right 1 time
            if left_turns == 3:
                self.turn_robot_right()
            else:
                for _ in range(left_turns):
                    self.turn_robot_left()
            self.move_robot()

    def move_robot(self):
        next_pos = self.calculate_next_pos()

        if not self.observed_map.get(next_pos['y'], None):
            self.observed_map[next_pos['y']] = {}

        if self.robot.move():
            # mark the point as visited
            self.observed_map[next_pos['y']][next_pos['x']] = 1
            self.current_position = next_pos
            if self.loggable:
                self.print_map()
            return True
        # mark the point as inaccessible
        self.observed_map[next_pos['y']][next_pos['x']] = -1
        if self.loggable:
            self.print_map()
        return False

    def calculate_next_pos(self):
        next_pos_x = self.current_position['x'] + cos(self.current_direction)
        next_pos_y = self.current_position['y'] - sin(self.current_direction)
        return {'x': next_pos_x, 'y': next_pos_y}

    def turn_robot_left(self):
        self.current_direction = (self.current_direction + 1) % 4
        self.robot.turn_left()

    def turn_robot_right(self):
        self.current_direction = (self.current_direction + 3) % 4
        self.robot.turn_right()

    def print_map(self):
        print_observed_map(self)

    def log(self, text):
        if self.loggable:
            print(text)
