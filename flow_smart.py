import heapq
import time

def init_maze(maze):

    # Read in the given file line by line until the end of file
    with open('14x14maze.txt', 'r') as file:
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

def check_spaces(maze, current_x, current_y, current_var):
    blocked = 0

    if (current_x - 1 >= 0 and maze[current_y][current_x - 1] == current_var):
        blocked += 1

    if (current_y - 1 >= 0 and maze[current_y - 1][current_x] == current_var):
        blocked += 1

    if (current_x + 1 < len(maze) and maze[current_y][current_x + 1] == current_var):
        blocked += 1

    if (current_y + 1 < len(maze) and maze[current_y + 1][current_x] == current_var):
        blocked += 1

    if blocked == 2:
        return True

    return False


def make_dead_end(maze, current_x, current_y, current_var):

    if ( (current_x - 1 >= 0 and maze[current_y][current_x - 1] == '_') and check_spaces(maze, current_x - 1, current_y, current_var) ):
        return True

    if ( (current_y - 1 >= 0 and maze[current_y - 1][current_x] == '_') and check_spaces(maze, current_x, current_y - 1, current_var) ):
        return True

    if ( (current_x + 1 < len(maze) and maze[current_y][current_x + 1] == '_') and check_spaces(maze, current_x + 1, current_y, current_var) ):
        return True

    if ( (current_y + 1 < len(maze) and maze[current_y + 1][current_x] == '_') and check_spaces(maze, current_x, current_y + 1, current_var) ):
        return True

    return False


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
    #print('Greedy start******************************************')
    while True:
        # First goal check the left node and if it matches, print path cost
        # If not a goal, then calculate its distance to goal and add it to the PQ
        if (current_x - 1 >= 0 and (current_x - 1 == final_x and current_y == final_y)):
            #print('Greedy Done With Solution******************************************')
            restore_maze(maze)
            #time.sleep(3)
            return True
        elif (current_x - 1 >= 0 and maze[current_y][current_x - 1] == '_'):
            path = distance_to_go(current_x - 1, current_y, final_x, final_y)
            heapq.heappush(g_pqueue, (path, [current_y, current_x - 1], g_path_cost + 1))
            maze[current_y][current_x - 1] = 'c'
            #print_maze(maze)

        # Then goal check the top node and if it matches, print path cost
        # If not a goal, then calculate its distance to goal and add it to the PQ
        if (current_y - 1 >= 0 and (current_x == final_x and current_y - 1 == final_y)):
            #print('Greedy Done With Solution******************************************')
            restore_maze(maze)
            #time.sleep(3)
            return True
        elif (current_y - 1 >= 0 and maze[current_y - 1][current_x] == '_'):
            path = distance_to_go(current_x, current_y - 1, final_x, final_y)
            heapq.heappush(g_pqueue, (path, [current_y - 1, current_x], g_path_cost + 1))
            maze[current_y - 1][current_x] = 'c'
            #print_maze(maze)

        # Goal check the right node and if it matches, print path cost
        # If not a goal, then calculate its distance to goal and add it to the PQ
        if (current_x + 1 < len(maze) and (current_x + 1 == final_x and current_y == final_y)):
            #print('Greedy Done With Solution******************************************')
            restore_maze(maze)
            #time.sleep(3)
            return True
        elif (current_x + 1 < len(maze) and maze[current_y][current_x + 1] == '_'):
            path = distance_to_go(current_x + 1, current_y, final_x, final_y)
            heapq.heappush(g_pqueue, (path, [current_y, current_x + 1], g_path_cost + 1))
            maze[current_y][current_x + 1] = 'c'
            #print_maze(maze)

        # Finally goal check the bottom node and if it matches, print path cost
        # If not a goal, then calculate its distance to goal and add it to the PQ
        if (current_y + 1 < len(maze) and (current_x == final_x and current_y + 1 == final_y)):
            #print('Greedy Done With Solution******************************************')
            restore_maze(maze)
            #time.sleep(3)
            return True
        elif (current_y + 1 < len(maze) and maze[current_y + 1][current_x] == '_'):
            path = distance_to_go(current_x, current_y + 1, final_x, final_y)
            heapq.heappush(g_pqueue, (path, [current_y + 1, current_x], g_path_cost + 1))
            maze[current_y + 1][current_x] = 'c'
            #print_maze(maze)

        # Update the old position with a '.' and update the current position
        # Also update the expanded node count and the node path cost
        if len(g_pqueue) > 0:
            current_node = heapq.heappop(g_pqueue)
            current_x = current_node[1][1]
            current_y = current_node[1][0]
            g_path_cost = current_node[2]
            #print_maze(maze)
        else:
            #print('Greedy Done With No Solution^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            #time.sleep(3)
            restore_maze(maze)
            return False

def backtrack(maze, current_var, start_x, start_y, current_x, current_y, final_x, final_y, i, vars):
    found = False
    if check_finished(maze):
        return True
    else:
        #print('Backtrack###############################################')
        if (current_y + 1 < len(maze) and (current_x == final_x and current_y + 1 == final_y)):
            if check_finished(maze):
                return True

            elif i == len(vars) - 1:
                maze[current_y][current_x] = '_'
                return False

            found = find_solution (maze, vars, i+1)

        if (current_x + 1 < len(maze) and (current_x + 1 == final_x and current_y == final_y)):
            if check_finished(maze):
                return True

            elif i == len(vars) - 1:
                maze[current_y][current_x] = '_'
                return False

            found = find_solution (maze, vars, i+1)

        if (current_y - 1 >= 0 and (current_x == final_x and current_y - 1 == final_y)):
            if check_finished(maze):
                return True

            elif i == len(vars) - 1:
                maze[current_y][current_x] = '_'
                return False

            found = find_solution (maze, vars, i+1)

        if (current_x - 1 >= 0 and (current_x - 1 == final_x and current_y == final_y)):
            if check_finished(maze):
                return True

            elif i == len(vars) - 1:
                maze[current_y][current_x] = '_'
                return False

            found = find_solution (maze, vars, i+1)


        if (current_x - 1 >= 0 and maze[current_y][current_x - 1] == '_'):
            #print('called left')
            no_solution = False
            if not zig_zag(maze, current_var, current_x - 1, current_y) and not make_dead_end(maze, current_x - 1, current_y, current_var):
                maze[current_y][current_x - 1] = current_var
                #print_maze(maze)
                for color in range(i+1, len(vars)):
                    temps_coords = find_var_start(maze, vars[color])
                    temps_x = temps_coords[0]
                    temps_y = temps_coords[1]
                    tempf_coords = find_var_final(maze, vars[color])
                    tempf_x = tempf_coords[0]
                    tempf_y = tempf_coords[1]

                    if not greedy_best_first(maze, temps_x, temps_y, tempf_x, tempf_y):
                        no_solution = True
                        maze[current_y][current_x - 1] = '_'
                        break
                if not no_solution:
                    found = backtrack(maze, current_var, start_x, start_y, current_x - 1, current_y, final_x, final_y, i, vars)

        if (current_y - 1 >= 0 and maze[current_y - 1][current_x] == '_'):
            #print('called top')
            no_solution = False
            if not zig_zag(maze, current_var, current_x, current_y - 1) and not make_dead_end(maze, current_x, current_y - 1, current_var):
                maze[current_y - 1][current_x] = current_var
                #print_maze(maze)
                for color in range(i+1, len(vars)):
                    temps_coords = find_var_start(maze, vars[color])
                    temps_x = temps_coords[0]
                    temps_y = temps_coords[1]
                    tempf_coords = find_var_final(maze, vars[color])
                    tempf_x = tempf_coords[0]
                    tempf_y = tempf_coords[1]

                    if not greedy_best_first(maze, temps_x, temps_y, tempf_x, tempf_y):
                        no_solution = True
                        maze[current_y - 1][current_x] = '_'
                        break
                if not no_solution:
                    found = backtrack(maze, current_var, start_x, start_y, current_x, current_y - 1, final_x, final_y, i, vars)


        if (current_x + 1 < len(maze) and maze[current_y][current_x + 1] == '_'):
            #print('called right')
            no_solution = False
            if not zig_zag(maze, current_var, current_x + 1, current_y) and not make_dead_end(maze, current_x + 1, current_y, current_var):
                maze[current_y][current_x + 1] = current_var
                #print_maze(maze)
                for color in range(i+1, len(vars)):
                    temps_coords = find_var_start(maze, vars[color])
                    temps_x = temps_coords[0]
                    temps_y = temps_coords[1]
                    tempf_coords = find_var_final(maze, vars[color])
                    tempf_x = tempf_coords[0]
                    tempf_y = tempf_coords[1]

                    if not greedy_best_first(maze, temps_x, temps_y, tempf_x, tempf_y):
                        no_solution = True
                        maze[current_y][current_x + 1] = '_'
                        break
                if not no_solution:
                    found = backtrack(maze, current_var, start_x, start_y, current_x + 1, current_y, final_x, final_y, i, vars)

        if (current_y + 1 < len(maze) and maze[current_y + 1][current_x] == '_'):
            #print('called down')
            no_solution = False
            if not zig_zag(maze, current_var, current_x, current_y + 1) and not make_dead_end(maze, current_x, current_y + 1, current_var):
                maze[current_y + 1][current_x] = current_var
                #print_maze(maze)
                for color in range(i+1, len(vars)):
                    temps_coords = find_var_start(maze, vars[color])
                    temps_x = temps_coords[0]
                    temps_y = temps_coords[1]
                    tempf_coords = find_var_final(maze, vars[color])
                    tempf_x = tempf_coords[0]
                    tempf_y = tempf_coords[1]

                    if not greedy_best_first(maze, temps_x, temps_y, tempf_x, tempf_y):
                        no_solution = True
                        maze[current_y + 1][current_x] = '_'
                        break

                if not no_solution:
                    found = backtrack(maze, current_var, start_x, start_y, current_x, current_y + 1, final_x, final_y, i, vars)

        if not found:
            if not (current_x == start_x and current_y == start_y):
                maze[current_y][current_x] = '_'
            return False

    return found

def find_solution (maze, vars, i):
    #print ('Starting color: ' + vars[i])
    #print_maze(maze)
    #time.sleep(5)
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
    #print ('Finishing color: ' + vars[i])
    #print_maze(maze)
    #time.sleep(5)
    return solution

def main():
    maze = []
    init_maze(maze)
    vars = init_vars(maze)

    find_solution(maze, vars, 0)
    print_maze(maze)

time1 = time.time()
main()
time2 = time.time()
run_time = time2 - time1
print('Run time in seconds = ' + str(run_time))
