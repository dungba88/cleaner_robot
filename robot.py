from utils import sin, cos

class Robot(object):

    def __init__(self, matrix, start_position, start_direction):
        self.matrix = matrix
        self.current_position = start_position
        self.current_direction = start_direction
        self.loggable = True
        self.__visited_position = {str(start_position['x']) + '_' + str(start_position['y']): 1}

    def turn_left(self):
        """turn 90 degree counter-clockwise"""
        self.current_direction = (self.current_direction + 1) % 4

    def turn_right(self):
        """turn 90 degree clockwise"""
        self.current_direction = (self.current_direction + 3) % 4

    def move(self):
        """move ahead"""
        next_pos_x = self.current_position['x'] + cos(self.current_direction)
        next_pos_y = self.current_position['y'] - sin(self.current_direction)
        if not self.__can_move(next_pos_x, next_pos_y):
            self.__visited_position[str(next_pos_x) + "_" + str(next_pos_y)] = -1
            return False
        self.current_position['x'] = next_pos_x
        self.current_position['y'] = next_pos_y
        self.__visited_position[str(next_pos_x) + "_" + str(next_pos_y)] = 1
        return True

    def __can_move(self, next_pos_x, next_pos_y):
        if next_pos_x < 0 or next_pos_y < 0:
            return False
        if next_pos_y >= len(self.matrix):
            return False
        if next_pos_x >= len(self.matrix[0]):
            return False
        return self.matrix[next_pos_y][next_pos_x] == 0

    def log(self):
        if not self.loggable:
            return

        for i in range(len(self.matrix)):
            text = ""
            for j in range(len(self.matrix[i])):
                if i == self.current_position['y'] and j == self.current_position['x']:
                    if self.current_direction == 0:
                        text += '>'
                    elif self.current_direction == 1:
                        text += '^'
                    elif self.current_direction == 2:
                        text += '<'
                    else:
                        text += 'v'
                elif self.__visited_position.get(str(j) + "_" + str(i), None) == 1:
                    text += '*'
                elif self.matrix[i][j] == 0:
                    text += '.'
                else:
                    text += '|'
            print(text)
        print('')
