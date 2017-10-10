def cos(direction):
    """naive implementation of cos"""
    return int(abs(2 - direction) - 1)

def sin(direction):
    """naive implementation of cos"""
    return int(1 - abs(direction - 1))

def print_observed_map(sweeper):
    min_y = min(sweeper.observed_map)
    min_dict_x = min(sweeper.observed_map, key=lambda x: min(sweeper.observed_map[x]))
    min_x = min(sweeper.observed_map[min_dict_x])
    max_y = max(sweeper.observed_map)
    max_dict_x = max(sweeper.observed_map, key=lambda x: max(sweeper.observed_map[x]))
    max_x = max(sweeper.observed_map[max_dict_x])

    for i in range(min_y, max_y + 1):
        text = ""
        for j in range(min_x, max_x + 1):
            item = sweeper.observed_map[i].get(j, None)
            if sweeper.current_position['x'] == j \
                    and sweeper.current_position['y'] == i:
                text += 'o'
            elif not item:
                text += ' '
            elif item == 1:
                text += '*'
            else:
                text += '|'
        print(text)
    print('')

def bfs(start_position, start_direction, finish_check_fn, adjacent_check_fn, spiral):
    # this is just simple BFS implementation
    checked = {}
    queue = []
    queue.append({'x': start_position['x'], 'y': start_position['y'], 'direction': None, 'parent': None})

    while queue:
        current = queue.pop(0)
        if current['direction'] is not None:
            start_direction = current['direction']
        finished = finish_check_fn(current)
        if finished:
            path = []
            while current['parent']:
                path.append(current['direction'])
                current = current['parent']
            return path
        for node in adjacent(current, start_direction, spiral):
            key = str(node['x']) + '_' + str(node['y'])
            if not checked.get(key, None) \
                    and adjacent_check_fn(node):
                checked[key] = 1
                queue.append(node)

def adjacent(current, start_direction, spiral):
    if spiral:
        if start_direction == 0:
            return [
                {'x': current['x'], 'y': current['y'] - 1, 'direction': 1, 'parent': current},
                {'x': current['x'] + 1, 'y': current['y'], 'direction': 0, 'parent': current},
                {'x': current['x'], 'y': current['y'] + 1, 'direction': 3, 'parent': current},
                {'x': current['x'] - 1, 'y': current['y'], 'direction': 2, 'parent': current}
            ]
        if start_direction == 1:
            return [
                {'x': current['x'] - 1, 'y': current['y'], 'direction': 2, 'parent': current},
                {'x': current['x'], 'y': current['y'] - 1, 'direction': 1, 'parent': current},
                {'x': current['x'] + 1, 'y': current['y'], 'direction': 0, 'parent': current},
                {'x': current['x'], 'y': current['y'] + 1, 'direction': 3, 'parent': current}
            ]
        if start_direction == 2:
            return [
                {'x': current['x'], 'y': current['y'] + 1, 'direction': 3, 'parent': current},
                {'x': current['x'] - 1, 'y': current['y'], 'direction': 2, 'parent': current},
                {'x': current['x'], 'y': current['y'] - 1, 'direction': 1, 'parent': current},
                {'x': current['x'] + 1, 'y': current['y'], 'direction': 0, 'parent': current}
            ]
    return [
        {'x': current['x'] + 1, 'y': current['y'], 'direction': 0, 'parent': current},
        {'x': current['x'], 'y': current['y'] + 1, 'direction': 3, 'parent': current},
        {'x': current['x'] - 1, 'y': current['y'], 'direction': 2, 'parent': current},
        {'x': current['x'], 'y': current['y'] - 1, 'direction': 1, 'parent': current}
    ]