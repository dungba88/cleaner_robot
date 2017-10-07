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

def bfs(start_position, finish_check_fn, adjacent_check_fn):
    # this is just simple BFS implementation
    checked = {}
    queue = []
    queue.append({'x': start_position['x'], 'y': start_position['y'], 'd': None, 'parent': None})

    while queue:
        current = queue.pop(0)
        finished = finish_check_fn(current)
        if finished:
            path = []
            while current['parent']:
                path.append(current['direction'])
                current = current['parent']
            return path
        for node in adjacent(current):
            key = str(node['x']) + '_' + str(node['y'])
            if not checked.get(key, None) \
                    and adjacent_check_fn(node):
                checked[key] = 1
                queue.append(node)

def adjacent(current):
    return [
        {'x': current['x'] + 1, 'y': current['y'], 'direction': 0, 'parent': current},
        {'x': current['x'], 'y': current['y'] + 1, 'direction': 3, 'parent': current},
        {'x': current['x'] - 1, 'y': current['y'], 'direction': 2, 'parent': current},
        {'x': current['x'], 'y': current['y'] - 1, 'direction': 1, 'parent': current}
    ]