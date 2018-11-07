import heapq
import time

def init_maze(maze):

    # Read in the given file line by line until the end of file
    with open('9x9maze.txt', 'r') as file:
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
    for y in range(0, len(maze)):
        for x in range(0, len(maze)):
            if maze[y][x] == 'c':
                maze[y][x] = '_'

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
            elif count == 0 and item == var:
                final_x += 1
                count += 1
            elif count == 1 and item == var:
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

def distance_to_go(current_x, current_y, final_x, final_y):
    return ( abs(current_x - final_x) ) + ( abs( ( -current_y ) - ( -final_y ) ) )

def zig_zag(maze, current_var, current_x, current_y):

    if (current_x - 1 >= 0 and maze[current_y][current_x - 1] == current_var):
        if (current_y - 1 >= 0 and maze[current_y - 1][current_x - 1] == current_var):
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

# Function to use the Greedy Best First Search Algorithm
def greedy_best_first(maze, current_x, current_y, final_x, final_y):

    # Priority Queue used by the Greedy algorithm
    g_pqueue = []
    g_path_cost = 0

    # Check and expand nodes (Clockwise Left to Right)
    # Continue checking until the goal is reached
    while True:

        # First goal check the left node and if it matches, print path cost
        # If not a goal, then calculate its distance to goal and add it to the PQ
        if (current_x - 1 >= 0 and (current_x - 1 == final_x and current_y == final_y)):
            restore_maze(maze)
            return True
        elif (current_x - 1 >= 0 and maze[current_y][current_x - 1] == '_'):
            path = distance_to_go(current_x - 1, current_y, final_x, final_y)
            heapq.heappush(g_pqueue, (path, [current_y, current_x - 1], g_path_cost + 1))
            maze[current_y][current_x - 1] = 'c'

        # Then goal check the top node and if it matches, print path cost
        # If not a goal, then calculate its distance to goal and add it to the PQ
        if (current_y - 1 >= 0 and (current_x == final_x and current_y - 1 == final_y)):
            restore_maze(maze)
            return True
        elif (current_y - 1 >= 0 and maze[current_y - 1][current_x] == '_'):
            path = distance_to_go(current_x, current_y - 1, final_x, final_y)
            heapq.heappush(g_pqueue, (path, [current_y - 1, current_x], g_path_cost + 1))
            maze[current_y - 1][current_x] = 'c'

        # Goal check the right node and if it matches, print path cost
        # If not a goal, then calculate its distance to goal and add it to the PQ
        if (current_x + 1 < len(maze) and (current_x + 1 == final_x and current_y == final_y)):
            restore_maze(maze)
            return True
        elif (current_x + 1 < len(maze) and maze[current_y][current_x + 1] == '_'):
            path = distance_to_go(current_x + 1, current_y, final_x, final_y)
            heapq.heappush(g_pqueue, (path, [current_y, current_x + 1], g_path_cost + 1))
            maze[current_y][current_x + 1] = 'c'

        # Finally goal check the bottom node and if it matches, print path cost
        # If not a goal, then calculate its distance to goal and add it to the PQ
        if (current_y + 1 < len(maze) and (current_x == final_x and current_y + 1 == final_y)):
            restore_maze(maze)
            return True
        elif (current_y + 1 < len(maze) and maze[current_y + 1][current_x] == '_'):
            path = distance_to_go(current_x, current_y + 1, final_x, final_y)
            heapq.heappush(g_pqueue, (path, [current_y + 1, current_x], g_path_cost + 1))
            maze[current_y + 1][current_x] = 'c'

        # Update the old position with a '.' and update the current position
        # Also update the expanded node count and the node path cost
        if len(g_pqueue) > 0:
            current_node = heapq.heappop(g_pqueue)
            current_x = current_node[1][1]
            current_y = current_node[1][0]
            g_path_cost = current_node[2]
        else:
            print('*********CALLED************')
            restore_maze(maze)
            return False

def backtrack(maze, current_var, start_x, start_y, current_x, current_y, final_x, final_y, i, vars):
    found = False
    if check_finished(maze):
        return True
    else:
        if (current_y + 1 < len(maze) and (current_x == final_x and current_y + 1 == final_y)):
            found = find_solution (maze, vars, i+1)

        if (current_x + 1 < len(maze) and (current_x + 1 == final_x and current_y == final_y)):
            found = find_solution (maze, vars, i+1)

        if (current_y - 1 >= 0 and (current_x == final_x and current_y - 1 == final_y)):
            found = find_solution (maze, vars, i+1)

        if (current_x - 1 >= 0 and (current_x - 1 == final_x and current_y == final_y)):
            found = find_solution (maze, vars, i+1)

        if (current_x - 1 >= 0 and maze[current_y][current_x - 1] == '_'):
            #print('called left')
            if not zig_zag(maze, current_var, current_x - 1, current_y):
                maze[current_y][current_x - 1] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x - 1, current_y, final_x, final_y, i, vars)

        if (current_y - 1 >= 0 and maze[current_y - 1][current_x] == '_'):
            #print('called top')
            if not zig_zag(maze, current_var, current_x, current_y - 1):
                maze[current_y - 1][current_x] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x, current_y - 1, final_x, final_y, i, vars)

        if (current_x + 1 < len(maze) and maze[current_y][current_x + 1] == '_'):
            #print('called right')
            if not zig_zag(maze, current_var, current_x + 1, current_y):
                maze[current_y][current_x + 1] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x + 1, current_y, final_x, final_y, i, vars)

        if (current_y + 1 < len(maze) and maze[current_y + 1][current_x] == '_'):
            #print('called down')
            if not zig_zag(maze, current_var, current_x, current_y + 1):
                maze[current_y + 1][current_x] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x, current_y + 1, final_x, final_y, i, vars)

        if not found:
            if not (current_x == start_x and current_y == start_y):
                maze[current_y][current_x] = '_'
            return False
    found = True
    return found

def find_solution (maze, vars, i):
    print ('Starting color: ' + vars[i])
    print_maze(maze)
    current_coords = find_var_start(maze, vars[i])
    final_coords = find_var_final(maze, vars[i])
    current_x = current_coords[0]
    current_y = current_coords[1]
    final_x = final_coords[0]
    final_y = final_coords[1]
    if greedy_best_first(maze, current_x, current_y, final_x, final_y):
        solution = backtrack(maze, vars[i], current_x, current_y, current_x, current_y, final_x, final_y, i, vars)
    else:
        return False
    print ('Finishing color: ' + vars[i])
    print_maze(maze)
    return solution

def main():
    maze = []
    init_maze(maze)
    vars = init_vars(maze)

    find_solution(maze, vars, 0)

time1 = time.time()
main()
time2 = time.time()
run_time = time2 - time1
print('Run time in seconds = ' + str(run_time))
