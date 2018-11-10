import heapq
import time

####################################################
# Function that sets up the maze into a 2D List
def init_maze(maze, filename):

    # Read in the given file line by line until the end of file
    with open(filename, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            maze.append(list(line))


####################################################
# Helper function that prints out the given maze
def print_maze(maze):

    for line in maze:
        for item in line:
            print(item, end='')
        print('\n')


#################################################
# Helper function that initializes the list of colors
def init_vars(maze):
    csp_vars = []
    vars_exits = []
    for y in range(0, len(maze)):
        for x in range(0, len(maze)):
            if maze[y][x] != '_' and maze[y][x] != '\n' and maze[y][x] not in csp_vars:
                exits = find_exits(maze, x, y)
                heapq.heappush(vars_exits, (exits, maze[y][x], (x, y)))

    csp_vars.append((vars_exits[0][1], vars_exits[0][2]))
    for (exit, color, coords) in vars_exits:
        present = False
        for tuple in csp_vars:
            if color in tuple:
                present = True
        if not present:
            csp_vars.append((color, coords))
    
    return csp_vars


def find_exits(maze, current_x, current_y):
    exits = 0
    if (current_x - 1 >= 0 and maze[current_y][current_x - 1] == '_'):
        exits += 1
    if (current_y - 1 >= 0 and maze[current_y - 1][current_x] == '_'):
        exits += 1
    if (current_x + 1 < len(maze) and maze[current_y][current_x + 1] == '_'):
        exits += 1
    if (current_y + 1 < len(maze) and maze[current_y + 1][current_x] == '_'):
        exits += 1
    
    return exits
    

#################################################
# Function used by Greedy search forward check
# that sets all checked spaces back to underscores
def restore_maze(maze):
    for y in range(0, len(maze)):
        for x in range(0, len(maze)):
            if maze[y][x] == 'c':
                maze[y][x] = '_'

#############################################
# Helper function that finds the finishing
# coordinates for a given color
def find_var_final(maze, var, start_x, start_y):

    for y in range(0, len(maze)):
        for x in range(0, len(maze)):
            if (maze[y][x] == var and (x != start_x or y != start_y)):
                return [x, y]


########################################
# Helper function that serves as the base
# case for the backtracking function
def check_finished(maze):
    for line in maze:
        for item in line:
            if item == '_':
                return False

    return True

##########################################
# Helper function that serves as the distance
# heuristic for the greedy forward checking
def distance_to_go(current_x, current_y, final_x, final_y):
    return ( abs(current_x - final_x) ) + ( abs( ( -current_y ) - ( -final_y ) ) )


############################################
# Helper function that checks if an empty space
# became a dead end during maze traversal
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


#######################################
# Helper function that checks if a dead end
# was made during a color's solution traversal
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


########################################
# Helper function that checks if moving to
# a given spot in the maze would cause a 
# disallowed zig zag patter
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

##################################################
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
            restore_maze(maze)
            return False


#####################################################
# Main Backtracking function that moves a color through
# the maze trying to find a solution
def backtrack(maze, current_var, start_x, start_y, current_x, current_y, final_x, final_y, i, vars):
    found = False
    
    # First check if the maze is completed and we can stop
    if check_finished(maze):
        return True
        
    # If the maze is not finished...
    else:
        
        # First check if the space to the bottom of the current position is the finishing space
        if (current_y + 1 < len(maze) and (current_x == final_x and current_y + 1 == final_y)):
            
            # If this solution completes the maze, search is done
            if check_finished(maze):
                return True

            # If not, a solution is incorrect somewhere, so keep going
            elif i == len(vars) - 1:
                maze[current_y][current_x] = '_'
                return False

            found = find_solution (maze, vars, i+1)

        # Then check space to the right for completion
        if (current_x + 1 < len(maze) and (current_x + 1 == final_x and current_y == final_y)):
            
            # If this solution completes the maze, search is done
            if check_finished(maze):
                return True

            # If not, a solution is incorrect somewhere, so keep going
            elif i == len(vars) - 1:
                maze[current_y][current_x] = '_'
                return False

            found = find_solution (maze, vars, i+1)

        # Then check the space above current position for completion
        if (current_y - 1 >= 0 and (current_x == final_x and current_y - 1 == final_y)):
            
            # If this solution completes maze, search is done
            if check_finished(maze):
                return True

            # If not, a solution is incorrect somewhere, so keep going
            elif i == len(vars) - 1:
                maze[current_y][current_x] = '_'
                return False

            found = find_solution (maze, vars, i+1)

        # Finally check if space to the left is a completed solution
        if (current_x - 1 >= 0 and (current_x - 1 == final_x and current_y == final_y)):
            
            # If this solution completes the maze, search is done
            if check_finished(maze):
                return True

            # If not, a solution is incorrect somewhere, so keep going
            elif i == len(vars) - 1:
                maze[current_y][current_x] = '_'
                return False

            found = find_solution (maze, vars, i+1)


        # Move on to check if space to the left is open
        if (current_x - 1 >= 0 and maze[current_y][current_x - 1] == '_'):
            no_solution = False
            
            # If moving to this space does not create a zig zag and does not make a dead end...
            if not zig_zag(maze, current_var, current_x - 1, current_y) and not make_dead_end(maze, current_x - 1, current_y, current_var):
                maze[current_y][current_x - 1] = current_var
                
                # Move to this space, then run the forward check greedy search
                # This ensures that every other color can reach its goal still
                # If a color fails this test, backtrack immediately
                for color in range(i+1, len(vars)):
                    temps_x = vars[color][1][0]
                    temps_y = vars[color][1][1]
                    tempf_coords = find_var_final(maze, vars[color][0], temps_x, temps_y)
                    tempf_x = tempf_coords[0]
                    tempf_y = tempf_coords[1]

                    if not greedy_best_first(maze, temps_x, temps_y, tempf_x, tempf_y):
                        no_solution = True
                        maze[current_y][current_x - 1] = '_'
                        break
                if not no_solution:
                    found = backtrack(maze, current_var, start_x, start_y, current_x - 1, current_y, final_x, final_y, i, vars)

        # Then check the space above to see if it is open
        if (current_y - 1 >= 0 and maze[current_y - 1][current_x] == '_'):
            no_solution = False
            
            # If moving to this space does not create a zig zag and does not make a dead end...
            if not zig_zag(maze, current_var, current_x, current_y - 1) and not make_dead_end(maze, current_x, current_y - 1, current_var):
                maze[current_y - 1][current_x] = current_var
                
                # Move to this space, then run the forward check greedy search
                # This ensures that every other color can reach its goal still
                # If a color fails this test, backtrack immediately
                for color in range(i+1, len(vars)):
                    temps_x = vars[color][1][0]
                    temps_y = vars[color][1][1]
                    tempf_coords = find_var_final(maze, vars[color][0], temps_x, temps_y)
                    tempf_x = tempf_coords[0]
                    tempf_y = tempf_coords[1]

                    if not greedy_best_first(maze, temps_x, temps_y, tempf_x, tempf_y):
                        no_solution = True
                        maze[current_y - 1][current_x] = '_'
                        break
                if not no_solution:
                    found = backtrack(maze, current_var, start_x, start_y, current_x, current_y - 1, final_x, final_y, i, vars)


        # Then check the space to the right to see if it is open
        if (current_x + 1 < len(maze) and maze[current_y][current_x + 1] == '_'):
            no_solution = False
            
            # If moving to this space does not create a zig zag and does not make a dead end...
            if not zig_zag(maze, current_var, current_x + 1, current_y) and not make_dead_end(maze, current_x + 1, current_y, current_var):
                maze[current_y][current_x + 1] = current_var
                
                # Move to this space, then run the forward check greedy search
                # This ensures that every other color can reach its goal still
                # If a color fails this test, backtrack immediately
                for color in range(i+1, len(vars)):
                    temps_x = vars[color][1][0]
                    temps_y = vars[color][1][1]
                    tempf_coords = find_var_final(maze, vars[color][0], temps_x, temps_y)
                    tempf_x = tempf_coords[0]
                    tempf_y = tempf_coords[1]

                    if not greedy_best_first(maze, temps_x, temps_y, tempf_x, tempf_y):
                        no_solution = True
                        maze[current_y][current_x + 1] = '_'
                        break
                if not no_solution:
                    found = backtrack(maze, current_var, start_x, start_y, current_x + 1, current_y, final_x, final_y, i, vars)

        # Finally, check to see if the space below the current position is open
        if (current_y + 1 < len(maze) and maze[current_y + 1][current_x] == '_'):
            no_solution = False
            
            # If moving to this space does not create a zig zag and does not make a dead end...
            if not zig_zag(maze, current_var, current_x, current_y + 1) and not make_dead_end(maze, current_x, current_y + 1, current_var):
                maze[current_y + 1][current_x] = current_var
                
                # Move to this space, then run the forward check greedy search
                # This ensures that every other color can reach its goal still
                # If a color fails this test, backtrack immediately
                for color in range(i+1, len(vars)):
                    temps_x = vars[color][1][0]
                    temps_y = vars[color][1][1]
                    tempf_coords = find_var_final(maze, vars[color][0], temps_x, temps_y)
                    tempf_x = tempf_coords[0]
                    tempf_y = tempf_coords[1]

                    if not greedy_best_first(maze, temps_x, temps_y, tempf_x, tempf_y):
                        no_solution = True
                        maze[current_y + 1][current_x] = '_'
                        break

                if not no_solution:
                    found = backtrack(maze, current_var, start_x, start_y, current_x, current_y + 1, final_x, final_y, i, vars)

        # If a solution was not found for the current color,
        # backtrack and keep searching
        if not found:
            if not (current_x == start_x and current_y == start_y):
                maze[current_y][current_x] = '_'
            return False

    return found

#####################################
# Function used to maintain a connection between
# the recursion stacks of the different colors
# in the maze
def find_solution (maze, vars, i):
    current_x = vars[i][1][0]
    current_y = vars[i][1][1]
    final_coords = find_var_final(maze, vars[i][0], current_x, current_y)
    final_x = final_coords[0]
    final_y = final_coords[1]
    if greedy_best_first(maze, current_x, current_y, final_x, final_y):
        solution = backtrack(maze, vars[i][0], current_x, current_y, current_x, current_y, final_x, final_y, i, vars)
    else:
        return False
    return solution

########################################
# Main function that initializes the maze,
# initializes the list of variables,
# and begins the searching
def main():
    maze = []
    
    # Menu that allows user to select a maze to run
    while True:
        print('Automated Flow Free Solver')
        print('---------------------------')
        print('Please select a maze to solve:')
        print('Enter 5 for 5x5 maze')
        print('Enter 7 for 7x7 maze')
        print('Enter 8 for 8x8 maze')
        print('Enter 9 for 9x9 maze')
        print('Enter 10 for 10x10 maze')
        print('Enter 12 for 12x12 maze')
        print('\n')
        name = input('Please select a maze: ')
        
        if (name == '5'):
            init_maze(maze, '5x5maze.txt')
            break
            
        elif (name == '7'):
            init_maze(maze, '7x7maze.txt')
            break
            
        elif (name == '8'):
            init_maze(maze, '8x8maze.txt')
            break
            
        elif (name == '9'):
            init_maze(maze, '9x9maze.txt')
            break
            
        elif (name == '10'):
            init_maze(maze, '10x10maze.txt')
            break
            
        elif (name == '12'):
            init_maze(maze, '12x12maze.txt')
            break
            
        else:
            print('Invalid maze input!')
            print('\n')
    
    vars = init_vars(maze)
    time1 = time.time()
    find_solution(maze, vars, 0)
    time2 = time.time()
    run_time = time2 - time1
    print('\n')
    print('Run time in seconds = ' + str(run_time))
    print('\n')
    print_maze(maze)


main()
