def init_maze(maze):

    # Read in the given file line by line until the end of file
    with open('5x5.txt', 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            maze.append(list(line))

# Helper function that prints out the given maze
def print_maze(maze):

    for line in maze:
        for item in line:
            print(item, end='')
        print('\n')

def init_vars(maze):
    csp_vars = []
    for line in maze:
        for item in line:
            if item != '_' and item != '\n' and item not in csp_vars:
                csp_vars.append(item)

    return csp_vars

def restore_maze(maze):
    for line in maze:
        for item in line:
            if item == 'c':
                item = '_'

def find_var_start(maze, var):
    start_x = 0
    start_y = 0

    for line in maze:
        for item in line:
            found_item = False

            if item == '_' or item != var:
                start_x += 1
            else:
                found_item = True
                break

        if not found_item:
            start_y += 1
            start_x = 0
        else:
            return [start_x, start_y]

    return None

def find_var_final(maze, var):
    final_x = 0
    final_y = 0
    count = 0

    for line in maze:
        for item in line:
            found_item = False

            if item == '_' or item != var:
                final_x += 1
            else:
                found_item = True
                count += 1
                break

        if not found_item or count < 2:
            final_y += 1
            final_x = 0
        else:
            return [final_x, final_y]

def check_finished(maze):
    for line in maze:
        for item in line:
            if item == '_':
                return False

    return True

def zig_zag(maze, current_var, current_x, current_y):

    if (current_x - 1 >= 0 and maze[current_y][current_x - 1] == current_var):
        if (current_y - 1 >= 0 and maze[current_x - 1][current_y - 1] == current_var):
            if (current_y - 1 >= 0 and maze[current_y - 1][current_x] == current_var):
                return True

    if (current_y - 1 >= 0 and maze[current_y - 1][current_x] == current_var):
        if (current_x + 1 < len(maze) and maze[current_y - 1][current_x + 1] == current_var):
            if (maze[current_y][current_x + 1] == current_var):
                return True

    if (current_x + 1 < len(maze) and maze[current_y][current_x + 1] == current_var):
        if (current_y + 1 < len(maze) and maze[current_y + 1][current_x + 1] == current_var):
            if (maze[current_y + 1][current_x] == current_var):
                return True

    if (current_y + 1 < len(maze) and maze[current_y + 1][current_x] == current_var):
        if (current_x - 1 >= 0 and maze[current_y + 1][current_x - 1] == current_var):
            if (maze[current_y][current_x - 1] == current_var):
                return True

    return False

# Function to use the A* Search Algorithm
def a_star(maze, var):

    # Priority Queue used by the Greedy algorithm
    a_pqueue = []

    # First find the location of the 'P' starting spot in maze
    # Then add it to the priority queue
    current_coords = find_var_start(maze, var)
    current_y = current_coords[1]
    current_x = current_coords[0]

    # Then find the location of the '*' starting spot in maze
    # Then add it to the priority queue
    final_coords = find_var_final(maze, var)
    final_y = final_coords[1]
    final_x = final_coords[0]
    goal = False
    old_path_traveled = 0

    # Check and expand nodes (Clockwise Left to Right)
    # Continue checking until the goal is reached
    while (not goal):

        # First goal check the left node
        # If not a goal, then calculate the sum of the distance to goal plus
        # the path cost to the current position
        if (current_x - 1 >= 0 and (current_x - 1 == final_x and current_y == final_y)):
            goal = True
            break
        elif (maze[current_y][current_x - 1] == '_'):
            path_traveled = old_path_traveled + 1
            path_to_go = distance_to_go(current_x - 1, current_y, star_x, star_y)
            path = path_traveled + path_to_go
            heapq.heappush(a_pqueue, (path, path_traveled, [current_y, current_x - 1]))
            maze[current_y][current_x] = 'c'

        # Then goal check the top node
        # If not a goal, then calculate the sum of the distance to goal plus
        # the path cost to the current position
        if (current_y - 1 >= 0 and (current_x == final_x and current_y - 1 == final_y)):
            goal = True
            break
        elif (maze[current_y - 1][current_x] == '_'):
            path_traveled = old_path_traveled + 1
            path_to_go = distance_to_go(current_x, current_y - 1, star_x, star_y)
            path = path_traveled + path_to_go
            heapq.heappush(a_pqueue, (path, path_traveled, [current_y - 1, current_x]))
            maze[current_y - 1][current_x] = 'c'

        # Goal check the right node
        # If not a goal, then calculate the sum of the distance to goal plus
        # the path cost to the current position
        if (current_x + 1 < len(maze) and (current_x + 1 == final_x and current_y == final_y):
            goal = True
            break
        elif (maze[current_y][current_x + 1] == '_'):
            path_traveled = old_path_traveled + 1
            path_to_go = distance_to_go(current_x + 1, current_y, star_x, star_y)
            path = path_traveled + path_to_go
            heapq.heappush(a_pqueue, (path, path_traveled, [current_y, current_x + 1]))
            maze[current_y][current_x + 1] = 'c'

        # Finally goal check the bottom node
        # If not a goal, then calculate the sum of the distance to goal plus
        # the path cost to the current position
        if (current_y + 1 < len(maze) and (current_x == final_x and current_y == final_y)):
            goal = True
            break
        elif (maze[current_y + 1][current_x] == ' '):
            path_traveled = old_path_traveled + 1
            path_to_go = distance_to_go(current_x, current_y + 1, star_x, star_y)
            path = path_traveled + path_to_go
            heapq.heappush(a_pqueue, (path, path_traveled, [current_y + 1, current_x]))
            maze[current_y + 1][current_x] = 'c'

        # Update the old position with a '.' and update the current position
        # Update the the path cost of the old position as well
        if len(heapq) > 0
            current_tuple = heapq.heappop(a_pqueue)
            a_expanded += 1
            maze[current_y][current_x] = '.'
            current_x = current_tuple[2][1]
            current_y = current_tuple[2][0]
            old_path_traveled = current_tuple[1]
        else:
            restore_maze(maze)
            return False

def backtrack(maze, current_var, start_x, start_y, current_x, current_y, final_x, final_y, i, vars):
    found = False
    if check_finished(maze):
        return True
    else:
        print_maze(maze)
        if (current_y + 1 < len(maze) and (current_x == final_x and current_y + 1 == final_y)):
            found = find_solution (maze, vars, i+1)

        if (current_x + 1 < len(maze) and (current_x + 1 == final_x and current_y == final_y)):
            found = find_solution (maze, vars, i+1)

        if (current_y - 1 >= 0 and (current_x == final_x and current_y - 1 == final_y)):
            found = find_solution (maze, vars, i+1)

        if (current_x - 1 >= 0 and (current_x - 1 == final_x and current_y == final_y)):
            found = find_solution (maze, vars, i+1)

        if (current_x - 1 >= 0 and maze[current_y][current_x - 1] == '_'):
            print('called left')
            if not zig_zag(maze, current_var, current_x - 1, current_y):
                maze[current_y][current_x - 1] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x - 1, current_y, final_x, final_y, i, vars)

        if (current_y - 1 >= 0 and maze[current_y - 1][current_x] == '_'):
            print('called top')
            if not zig_zag(maze, current_var, current_x, current_y - 1):
                maze[current_y - 1][current_x] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x, current_y - 1, final_x, final_y, i, vars)

        if (current_x + 1 < len(maze) and maze[current_y][current_x + 1] == '_'):
            print('called right')
            if not zig_zag(maze, current_var, current_x + 1, current_y):
                maze[current_y][current_x + 1] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x + 1, current_y, final_x, final_y, i, vars)

        if (current_y + 1 < len(maze) and maze[current_y + 1][current_x] == '_'):
            print('called down')
            if not zig_zag(maze, current_var, current_x, current_y + 1):
                maze[current_y + 1][current_x] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x, current_y + 1, final_x, final_y, i, vars)

        if not found:
            if not (current_x == start_x and current_y == start_y):
                maze[current_y][current_x] = '_'
            return False
    found = True
    print_maze(maze)
    return found

def find_solution (maze, vars, i):
    print ('Starting color: ' + vars[i])
    current_coords = find_var_start(maze, vars[i])
    final_coords = find_var_final(maze, vars[i])
    current_x = current_coords[0]
    current_y = current_coords[1]
    final_x = final_coords[0]
    final_y = final_coords[1]
    if a_star(maze, vars[i]):
        solution = backtrack(maze, vars[i], current_x, current_y, current_x, current_y, final_x, final_y, i, vars)
    else:
        return False
    print ('Finishing color: ' + vars[i])
    return solution

def main():
    maze = []
    init_maze(maze)
    vars = init_vars(maze)

    find_solution(maze, vars, 0)

main()
