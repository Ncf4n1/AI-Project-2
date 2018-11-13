import time


assignments = 0     # Variable for the number of attempted assignments

#############################
# Helper function to initliaze the text file
# into a 2D maze
def init_maze(maze, filename):

    # Read in the given file line by line until the end of file
    with open(filename, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            maze.append(list(line))


#####################################
# Helper function to write the puzzle
# solution to an output file
def write_to_file(maze, runtime, assignments):
    
    # Write out to a new output file
    file = open('maze_output.txt', 'a')
    for line in maze:
        for item in line:
            file.write(item)
    file.write('\n')
    file.write('Number of attempted assignments = ' + str(assignments) + '\n')
    file.write('Run time in seconds: ' + str(runtime))
    file.write('\n')
    file.write('\n')
    file.write('\n')
        
        
##############################################
# Helper function that prints out the given maze
def print_maze(maze):

    for line in maze:
        for item in line:
            print(item, end='')
        print('\n')


###############################################
# Helper function to create the list of colors
def init_vars(maze):
    csp_vars = []
    for line in maze:
        for item in line:
            if item != '_' and item != '\n' and item not in csp_vars:
                csp_vars.append(item)

    return csp_vars


###########################################
# Helper function to find the starting coordinates
# for the given color
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


##################################
# Helper function to find the ending
# coordinates for the given color
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


#######################################
# Helper function that checks if the 
# maze was completed when a solution is found
def check_finished(maze):
    for line in maze:
        for item in line:
            if item == '_':
                return False

    return True

##########################################
# Helper function used to determine if moving
# to a spot creates a zig zag pattern
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


#################################################
# Main backtracking function that depth first searches
# for a solution for the given maze
def backtrack(maze, current_var, start_x, start_y, current_x, current_y, final_x, final_y, i, vars):
    found = False
    global assignments
    
    # Base Case: Check if the maze was completed
    if check_finished(maze):
        return True
        
    # If not...
    else:
        
        # First check if the spot below you is the finishing spot
        # If so, unwind recursion stack
        if (current_y + 1 < len(maze) and (current_x == final_x and current_y + 1 == final_y)):
            found = find_solution (maze, vars, i+1)

        # Then check if the spot to the right is the finishing spot and repeat
        if (current_x + 1 < len(maze) and (current_x + 1 == final_x and current_y == final_y)):
            found = find_solution (maze, vars, i+1)

        # Check the spot above for finishing state
        if (current_y - 1 >= 0 and (current_x == final_x and current_y - 1 == final_y)):
            found = find_solution (maze, vars, i+1)

        # Finally, check the spot to the left for a finishing state
        if (current_x - 1 >= 0 and (current_x - 1 == final_x and current_y == final_y)):
            found = find_solution (maze, vars, i+1)

        # If no finish for the current color found,
        # begin by checking the left space to see if it is open
        if (current_x - 1 >= 0 and maze[current_y][current_x - 1] == '_'):
            
            # If the spot is open, check if moving there creates a zig zag pattern
            if not zig_zag(maze, current_var, current_x - 1, current_y):
                
                # If not move there and recursively move on
                assignments += 1
                maze[current_y][current_x - 1] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x - 1, current_y, final_x, final_y, i, vars)

        # Repeat the above process for the space above
        if (current_y - 1 >= 0 and maze[current_y - 1][current_x] == '_'):
            if not zig_zag(maze, current_var, current_x, current_y - 1):
                assignments += 1
                maze[current_y - 1][current_x] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x, current_y - 1, final_x, final_y, i, vars)

        # Repeat again for the space to the right
        if (current_x + 1 < len(maze) and maze[current_y][current_x + 1] == '_'):
            if not zig_zag(maze, current_var, current_x + 1, current_y):
                assignments += 1
                maze[current_y][current_x + 1] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x + 1, current_y, final_x, final_y, i, vars)

        # Finally, check the space below
        if (current_y + 1 < len(maze) and maze[current_y + 1][current_x] == '_'):
            if not zig_zag(maze, current_var, current_x, current_y + 1):
                assignments += 1
                maze[current_y + 1][current_x] = current_var
                found = backtrack(maze, current_var, start_x, start_y, current_x, current_y + 1, final_x, final_y, i, vars)

        # If a solution is dead without reaching its goal,
        # recursively backtrack and find a new solution
        if not found:
            if not (current_x == start_x and current_y == start_y):
                maze[current_y][current_x] = '_'
            return False

    return found


#######################################
# Main function that keeps each color's
# recursive stack together to finish the maze
def find_solution (maze, vars, i):
    current_coords = find_var_start(maze, vars[i])
    final_coords = find_var_final(maze, vars[i])
    current_x = current_coords[0]
    current_y = current_coords[1]
    final_x = final_coords[0]
    final_y = final_coords[1]
    solution = backtrack(maze, vars[i], current_x, current_y, current_x, current_y, final_x, final_y, i, vars)
    return solution

#######################################
# Main function that begins the flow solution
def main():
    maze = []
    global assignments
    
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
    print('Number of attempted assignments = ' + str(assignments))
    print('Run time in seconds = ' + str(run_time))
    print('\n')
    print_maze(maze)
    write_to_file(maze, run_time, assignments)


main()
