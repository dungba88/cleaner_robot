class Application {

    constructor(rows, cols, obstacles, canvas_id, pointer_id, target_id) {
        this.rows = rows;
        this.cols = cols;
        this.obstacles = obstacles;
        this.canvas_id = canvas_id;
        this.pointer_id = pointer_id;
        this.target_id = target_id;
        this.canvas = null;
        this.pointer = null;
    }
    
    load_app() {
        this.canvas = document.getElementById(this.canvas_id);
        this.pointer = document.getElementById(this.pointer_id);
        var ctx = this.canvas.getContext('2d');
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.draw_grid(ctx);
    }

    draw_obstacle(matrix) {
        let width = this.canvas.width;
        let height = this.canvas.height;

        let row_height = height / this.rows;
        let col_width = width / this.cols;

        var ctx = this.canvas.getContext('2d');

        for(let i = 0; i < matrix.length; i++) {
            for(let j = 0; j < matrix[i].length; j++) {
                if (matrix[i][j] != 0) {
                    ctx.fillRect(j * col_width, i * row_height, col_width, row_height);
                }
            }
        }
    }

    begin() {
        var ctx = this.canvas.getContext('2d');
        ctx.beginPath();
    }

    finish() {
        var ctx = this.canvas.getContext('2d');
        ctx.stroke();
    }

    update_position(robot, first_time) {
        let width = this.canvas.width;
        let height = this.canvas.height;

        let row_height = height / this.rows;
        let col_width = width / this.cols;

        let x = (robot.current_position.x + 0.5) * col_width;
        let y = (robot.current_position.y + 0.5) * row_height;
        
        var ctx = this.canvas.getContext('2d');
        if (first_time)
            ctx.moveTo(x, y);
        else
            ctx.lineTo(x, y);
        
        this.pointer.style.transform = 'translate('+x+'px, '+y+'px)';
        ctx.strokeStyle = '#ff0000';
        ctx.stroke();
    }

    update_target(current) {
        let width = this.canvas.width;
        let height = this.canvas.height;

        let row_height = height / this.rows;
        let col_width = width / this.cols;

        let x = (current.x + 0.5) * col_width;
        let y = (current.y + 0.5) * row_height;

        document.getElementById(this.target_id).style.left = x+'px';
        document.getElementById(this.target_id).style.top = y+'px';
    }
    
    draw_grid(ctx) {
        let width = this.canvas.width;
        let height = this.canvas.height;

        let row_height = height / this.rows;
        let col_width = width / this.cols;
        ctx.strokeStyle = '#000000';
        
        for(let i = 1; i < this.rows; i++) {
            ctx.beginPath();
            ctx.moveTo(0, i * row_height);
            ctx.lineTo(width, i * row_height);
            ctx.stroke();
        }

        for(let i = 1; i < this.cols; i++) {
            ctx.beginPath();
            ctx.moveTo(i * col_width, 0);
            ctx.lineTo(i * col_width, height);
            ctx.stroke();
        }
    }    
}

class Robot {

    constructor(matrix, start_position, start_direction, app) {
        this.matrix = matrix;
        this.start_position = {x: start_position.x, y: start_position.y};
        this.current_position = {x: start_position.x, y: start_position.y};
        this.start_direction = start_direction;
        this.current_direction = start_direction;
        this.loggable = false;
        this.app = app;
        this.move_count = 0;
        this.turn_count = 0;
        this.__visited_position = {};
        this.app.update_position(this, true);
        this.move_time = 100;
    }

    turn_left() {
        this.current_direction = (this.current_direction + 1) % 4;
        this.turn_count++;
        return this;
    }

    turn_right() {
        this.current_direction = (this.current_direction + 3) % 4;
        this.turn_count++;
        return this;
    }

    move() {
        let next_pos_x = this.current_position.x + ncos(this.current_direction);
        let next_pos_y = this.current_position.y - nsin(this.current_direction);
        if (!this.__can_move(next_pos_x, next_pos_y)) {
            this.__visited_position[next_pos_x + "_" + next_pos_y] = -1;
            return Promise.reject();
        }
        this.move_count++;
        this.current_position.x = next_pos_x;
        this.current_position.y = next_pos_y;
        this.__visited_position[next_pos_x + "_" + next_pos_y] = 1;
        if (this.loggable)
            this.log();
        this.app.update_position(this);
        return new Promise(resolve => {
            setTimeout(function() {
                resolve();
            }, this.move_time);
        });
    }

    __can_move(next_pos_x, next_pos_y) {
        if (next_pos_x < 0 || next_pos_y < 0)
            return false;
        if (next_pos_y >= this.matrix.length)
            return false;
        if (next_pos_x >= this.matrix[0].length)
            return false;
        return this.matrix[next_pos_y][next_pos_x] == 0;
    }

    log() {
        for(let i in this.matrix) {
            let text = "";
            for(let j in this.matrix[i]) {
                if (i == this.current_position.y && j == this.current_position.x) {
                    if (this.current_direction == 0)
                        text += '>';
                    else if (this.current_direction == 1)
                        text += '^';
                    else if (this.current_direction == 2)
                        text += '<';
                    else
                        text += 'v';
                } else if (this.__visited_position[j + "_" + i] == 1) {
                    text += '*';
                } else if (this.matrix[i][j] == 0) {
                    text += '.';
                } else {
                    text += '|';
                }
            }
            console.log(text);
        }
    }
}

class Sweeper {
    constructor(robot) {
        this.current_direction = 0;
        this.current_position = {x: 0, y: 0};
        this.observed_map = {0: {0: 1}};
        this.robot = robot;
        this.loggable = false;
        this.spiral = false;
    }

    sweep(callback) {
        this.move(function() {
            this.sweep(callback);
        }.bind(this), function() {
            // finished
            callback();
        })
    }

    move(success, fail) {
        this.log('looking for nearest unvisited position');
        let target_path = this.find_nearest_unvisited_pos();
        if (!target_path) {
            this.log('cannot find nearest unvisited position, cleaned');
            fail();
            return false;
        }
        this.log('found nearest unvisited position, moving there');
        this.update_target(target_path.current);
        this.move_with_path(target_path.path, success);
        return true;
    }

    update_target(current) {
        let _current = {x: current.x, y: current.y};
        if (this.robot.start_direction == 1) {
            let tmp = _current.x;
            _current.x = _current.y;
            _current.y = -tmp;
        } else if (this.robot.start_direction == 2) {
            _current.x = -_current.x;
            _current.y = -_current.y;
        } else if (this.robot.start_direction == 3) {
            let tmp = _current.x;
            _current.x = -_current.y;
            _current.y = tmp;
        }
        this.robot.app.update_target({
            x: _current.x + this.robot.start_position.x,
            y: _current.y + this.robot.start_position.y
        });
    }

    find_nearest_unvisited_pos() {
        return bfs(this.current_position, this.current_direction, this.spiral, this.node_unvisited.bind(this), this.adjacent_movable.bind(this));
    }

    node_unvisited(node) {
        return this.get_node_from_map(node) == null;
    }

    adjacent_movable(node) {
        return this.get_node_from_map(node) != -1;
    }

    get_node_from_map(node) {
        if (this.observed_map[node.y] == null
                || this.observed_map[node.y][node.x] == null)
            return null;
        return this.observed_map[node.y][node.x];
    }

    move_with_path(target_path, callback) {
        this.move_async(target_path, target_path.length - 1, callback);
    }

    move_async(target_path, i, callback) {
        if (i < 0) {
            callback();
            return;
        }
        let path = target_path[i];
        let left_turns = path - this.current_direction;
        if (left_turns < 0)
            left_turns += 4
        if (left_turns == 3) {
            this.turn_robot_right();
        } else {
            for(let i = 0; i < left_turns; i++) {
                this.turn_robot_left();
            }
        }
        this.move_robot(function() {
            this.move_async(target_path, i - 1, callback);
        }.bind(this));
    }

    async move_robot(callback) {
        let next_pos = this.calculate_next_pos();
        if (this.observed_map[next_pos.y] == null)
            this.observed_map[next_pos.y] = {};
    
        try {
            await this.robot.move();
            this.observed_map[next_pos.y][next_pos.x] = 1;
            this.current_position = next_pos;
            if (this.loggable)
                this.print_map();
            callback(true);
        } catch (ex) {
            this.observed_map[next_pos.y][next_pos.x] = -1;
            if (this.loggable)
                this.print_map();
            callback(false);
        }
    }

    calculate_next_pos() {
        let next_pos_x = this.current_position.x + ncos(this.current_direction);
        let next_pos_y = this.current_position.y - nsin(this.current_direction);
        return {x: next_pos_x, y: next_pos_y};
    }

    turn_robot_left() {
        this.current_direction = (this.current_direction + 1) % 4;
        this.robot.turn_left();
    }

    turn_robot_right() {
        this.current_direction = (this.current_direction + 3) % 4;
        this.robot.turn_right();
    }

    print_map() {
        // print_observed_map(self)
    }

    log(text) {
        if (this.loggable)
            console.log(text);
    }
}

class DFSSweeper {
    constructor(robot) {
        this.observed_map = {};
        this.robot = robot;
    }

    async sweep(callback) {
        await this.move({'x': 0, 'y': 0}, 0);
        callback();
    }

    async move(cur, dir) {
        this.observed_map[cur.x+'_'+cur.y] = 1;
        let straight = this.next_straight(cur, dir);
        if (!this.visited(straight)) {
            try {
                await this.robot.move();
                await this.move(straight, dir);
            } catch(ex) {}
        }

        let right = this.next_right(cur, dir);
        this.robot.turn_right();
        if (!this.visited(right)) {
            try {
                await this.robot.move();
                await this.move(right, (dir+1)%4);
            } catch(ex) {}
        }

        let down = this.next_down(cur, dir);
        this.robot.turn_right()
        if (!this.visited(down)) {
            try {
                await this.robot.move();
                await this.move(down, (dir+2)%4);
            } catch(ex) {}
        }

        let left = this.next_left(cur, dir);
        this.robot.turn_right();
        if (!this.visited(left)) {
            try {
                await this.robot.move();
                await this.move(left, (dir+3)%4);
            } catch(ex) {}
        }

        this.robot.turn_left();
        try {
            await this.robot.move();
            this.robot.turn_left().turn_left();
        } catch (ex) {}
    }

    next_straight(cur, dir) {
        return {'x': cur['x'] - ((dir + 1) % 2) * (dir - 1), 'y': cur['y'] - (dir % 2) * (dir - 2)};
    }

    next_right(cur, dir) {
        return {'x': cur['x'] + (dir % 2) * (dir - 2), 'y': cur['y'] - ((dir + 1) % 2) * (dir - 1)};
    }

    next_left(cur, dir) {
        return {'x': cur['x'] - (dir % 2) * (dir - 2), 'y': cur['y'] + ((dir + 1) % 2) * (dir - 1)};
    }

    next_down(cur, dir) {
        return {'x': cur['x'] + ((dir + 1) % 2) * (dir - 1), 'y': cur['y'] + (dir % 2) * (dir - 2)};
    }

    visited(node) {
        return this.observed_map[node.x+'_'+node.y] != null;
    }
}

function ncos(direction) {
    return Math.abs(2 - direction) - 1;
}

function nsin(direction) {
    return 1 - Math.abs(direction - 1);
}
// def print_observed_map(sweeper):
// min_y = min(sweeper.observed_map)
// min_dict_x = min(sweeper.observed_map, key=lambda x: min(sweeper.observed_map[x]))
// min_x = min(sweeper.observed_map[min_dict_x])
// max_y = max(sweeper.observed_map)
// max_dict_x = max(sweeper.observed_map, key=lambda x: max(sweeper.observed_map[x]))
// max_x = max(sweeper.observed_map[max_dict_x])

// for i in range(min_y, max_y + 1):
//     text = ""
//     for j in range(min_x, max_x + 1):
//         item = sweeper.observed_map[i].get(j, None)
//         if sweeper.current_position['x'] == j \
//                 and sweeper.current_position['y'] == i:
//             text += 'o'
//         elif not item:
//             text += ' '
//         elif item == 1:
//             text += '*'
//         else:
//             text += '|'
//     print(text)
// print('')

function bfs(start_position, start_direction, spiral, finish_check_fn, adjacent_check_fn) {
    let checked = {}
    let queue = []
    queue.push({
        x: start_position.x,
        y: start_position.y,
        direction: null,
        parent: null
    });
    
    while(queue.length > 0) {
        let current = queue.shift();
        if (current.direction != null)
            start_direction = current.direction;
        if (finish_check_fn(current)) {
            let path = [];
            let _current = current;
            while(current.parent) {
                path.push(current.direction);
                current = current.parent;
            }
            return {
                path: path,
                current: _current
            };
        }
        let adjacents = adjacent(current, start_direction, spiral);
        for(let i in adjacents) {
            let node = adjacents[i];
            let key = node.x + '_' + node.y;
            if (!checked[key] && adjacent_check_fn(node)) {
                checked[key] = 1;
                queue.push(node);
            }
        }
    }
}

function adjacent(current, start_direction, spiral) {
    if (spiral) {
        if (start_direction == 0) {
            return [
                {x: current.x, 'y': current.y - 1, 'direction': 1, 'parent': current},
                {x: current.x + 1, 'y': current.y, 'direction': 0, 'parent': current},
                {x: current.x, 'y': current.y + 1, 'direction': 3, 'parent': current},
                {x: current.x - 1, 'y': current.y, 'direction': 2, 'parent': current}
            ]
        }
        if (start_direction == 1) {
            return [
                {x: current.x - 1, 'y': current.y, 'direction': 2, 'parent': current},
                {x: current.x, 'y': current.y - 1, 'direction': 1, 'parent': current},
                {x: current.x + 1, 'y': current.y, 'direction': 0, 'parent': current},
                {x: current.x, 'y': current.y + 1, 'direction': 3, 'parent': current}
            ]
        }
        if (start_direction == 2) {
            return [
                {x: current.x, 'y': current.y + 1, 'direction': 3, 'parent': current},
                {x: current.x - 1, 'y': current.y, 'direction': 2, 'parent': current},
                {x: current.x, 'y': current.y - 1, 'direction': 1, 'parent': current},
                {x: current.x + 1, 'y': current.y, 'direction': 0, 'parent': current}
            ]
        }
    }
    return [
        {x: current.x + 1, 'y': current.y, 'direction': 0, 'parent': current},
        {x: current.x, 'y': current.y + 1, 'direction': 3, 'parent': current},
        {x: current.x - 1, 'y': current.y, 'direction': 2, 'parent': current},
        {x: current.x, 'y': current.y - 1, 'direction': 1, 'parent': current}
    ]
}