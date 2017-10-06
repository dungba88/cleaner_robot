from utils import sin, cos

class Sweeper(object):
    def __init__(self, robot):
        self.current_direction = 0
        self.current_position = {'x': 0, 'y': 0}
        self.count = 0
        self.observed_map = {0: {0: 1}}
        self.robot = robot
        self.loggable = True

    def sweep(self):
        self.count = 0
        self.observed_map = {0: {0: 1}}

        while True:
            if self.move():
                break

        return self.count

    def move(self):
        self.move_robot()
        #if self.move_robot():
        #    return False

        self.log('cant move, looking for nearest unvisited position')
        target_path = self.find_nearest_unvisited_pos()
        if not target_path:
            self.log('cannot find nearest unvisited position, cleaned')
            return True
        self.log('found nearest unvisited position, moving there')
        self.move_with_path(target_path)
        return False

    def log(self, text):
        if self.loggable:
            print(text)

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

    def move_robot(self):
        next_pos = self.calculate_next_pos()

        if not self.observed_map.get(next_pos['y'], None):
            self.observed_map[next_pos['y']] = {}

        if self.robot.move():
            self.count += 1
            self.observed_map[next_pos['y']][next_pos['x']] = 1
            self.current_position = next_pos
            if self.loggable:
                self.print_map()
            return True
        self.observed_map[next_pos['y']][next_pos['x']] = -1
        if self.loggable:
            self.print_map()
        return False

    def find_nearest_unvisited_pos(self):
        # this is just simple BFS implementation
        checked = {}
        queue = []
        queue.append({'x': self.current_position['x'], 'y': self.current_position['y'], 'd': None, 'parent': None})

        while queue:
            current = queue.pop(0)
            map_node = self.get_node_from_map(current)
            if not map_node:
                path = []
                while current['parent']:
                    path.append(current['d'])
                    current = current['parent']
                return path
            for node in self.adjacent(current):
                key = str(node['x']) + '_' + str(node['y'])
                map_node = self.get_node_from_map(node)
                if not checked.get(key, None) \
                        and map_node != -1:
                    checked[key] = 1
                    queue.append(node)

    def get_node_from_map(self, node):
        if not node['y'] in self.observed_map \
                or not node['x'] in self.observed_map[node['y']]:
            return None
        return self.observed_map[node['y']][node['x']]

    def adjacent(self, current):
        return [
            {'x': current['x'] + 1, 'y': current['y'], 'd': 0, 'parent': current},
            {'x': current['x'], 'y': current['y'] + 1, 'd': 3, 'parent': current},
            {'x': current['x'] - 1, 'y': current['y'], 'd': 2, 'parent': current},
            {'x': current['x'], 'y': current['y'] - 1, 'd': 1, 'parent': current}
        ]

    def move_with_path(self, target_path):
        for path in reversed(target_path):
            left_turns = path - self.current_direction
            if left_turns < 0:
                left_turns = left_turns + 4
            for i in range(left_turns):
                self.turn_robot_left()
            self.move_robot()

    def print_map(self):
        min_y = min(self.observed_map)
        min_dict_x = min(self.observed_map, key=self.get_min_x)
        min_x = min(self.observed_map[min_dict_x])
        max_y = max(self.observed_map)
        max_dict_x = max(self.observed_map, key=self.get_max_x)
        max_x = max(self.observed_map[max_dict_x])

        for i in range(min_y, max_y + 1):
            text = ""
            for j in range(min_x, max_x + 1):
                item = self.observed_map[i].get(j, None)
                if self.current_position['x'] == j \
                        and self.current_position['y'] == i:
                    text += 'o'
                elif not item:
                    text += ' '
                elif item == 1:
                    text += '*'
                else:
                    text += '|'
            print(text)
        print('')

    def get_min_x(self, x):
        return min(self.observed_map[x])

    def get_max_x(self, x):
        return max(self.observed_map[x])
