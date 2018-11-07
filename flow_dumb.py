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
    print(final_coords)
    final_x = final_coords[0]
    final_y = final_coords[1]
    solution = backtrack(maze, vars[i], current_x, current_y, current_x, current_y, final_x, final_y, i, vars)
    print ('Finishing color: ' + vars[i])
    return solution

def main():
    maze = []
    init_maze(maze)
    vars = init_vars(maze)

    find_solution(maze, vars, 0)

main()
