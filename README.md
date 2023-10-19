# Cleaning Robot Algorithms

This is simple cleaning robot algorithm written in Python. It assumes the following:

- Map can be interpreted as 2-d grid, with obstacles as obstructed points in the map.
- Obstacles can be arbitrary, both in quantity and position.
- The algorithm knows nothing about the surrounding environment.
- The robot only provides 3 API: turn_left, turn_right (rotate the looking direction) and move (move ahead 1 point)

The goal of the algorithm is to make the robot travel around room, with any point in the room visited at least one.

# how does it work

The algorithm (sweeper.py) works as follow:

1. Initialize the observed map to empty, current position to (0, 0)
2. Find the nearest unvisited point in observed map using Breadth-First Search
3. If cannot find, algorithm stops, and the accessible part of the room has been cleaned. Otherwise go to step 4
4. Move the robot to the position found in step 2, with each step updating the current position.
5. If it cannot move to the desired position, mark the position as obstructed in observed map, otherwise mark it as visited.
5. Go back to step 2

# how to use

```python
# matrix is a 2d array, with 0 indicating unobstructed, and anything else indicating obstructed
robot = Robot(matrix, start_position, start_direction)
sweeper = Sweeper(robot)
sweeper.sweep()
```

# complexity

Theoretically, the time complexity of the algorithm is O(N<sup>2</sup>). It need to find at most N unvisited points, and each needs at most N steps to get there. But in practice, since it only find the nearest unvisited position, so it can efficiently do it in O(N).

The space complexity is O(N), to store the observed map.

# optimization

An optimized version of the algorithm, called Spiral BFS, can help to reduce the number of steps taken by 5-10%. When visualizing the algorithm, I found out that the robot occasionally misses the uncleaned part (since it favors moving in one absolute direction), and needs to waste time traveling back. By making the robot favoring turning left (or right), it will minimize the chance of missing uncleaned parts. Two modes can be switched easily by setting `spiral` attribute of the algorithm

```python
sweeper.spiral = True
```

# demo

A demonstration can be found in https://jsfiddle.net/961uhtcy/

The code for the demonstration is placed under `showdown/` folder. It will compare the efficiency of different algorithms in randomly generated matrices.
