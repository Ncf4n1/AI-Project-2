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
            if item != '_' and item not in csp_vars:
                csp_vars.append(item)

    return csp_vars

def find_start(maze):
    start_x = 0
    start_y = 0

    for line in maze:
        for item in line:
            found_item = False

            if item == '_':
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

def check_finished(maze):
    for line in maze:
        for item in line:
            if item == '_':
                return False

    return True

def backtrack(maze, current_var, current_x, current_y):
    if check_finished(maze):
        return
    else:
        print_maze(maze)
        if ( current_x - 1 >= 0 and maze[current_y][current_x - 1] == '_'):
            print('called 1')
            maze[current_y][current_x - 1] = current_var
            current_x = current_x - 1

        elif ( current_y - 1 >= 0 and maze[current_y - 1][current_x] == '_'):
            print('called 2')
            maze[current_y - 1][current_x] = current_var
            current_y = current_y - 1

        elif ( current_x + 1 <= len(maze) and maze[current_y][current_x + 1] == '_'):
            print('called 3')
            maze[current_y][current_x + 1] = current_var
            current_x = current_x + 1

        elif ( current_y + 1 <= len(maze) and maze[current_y + 1][current_x] == '_'):
            print('called 4')
            maze[current_y + 1][current_x] = current_var
            current_y = current_y + 1
        else:
            return
            
        backtrack(maze, current_var, current_x, current_y)

def main():
    maze = []
    init_maze(maze)
    vars = init_vars(maze)
    start = find_start(maze)
    backtrack(maze, vars[0], start[0], start[1])

main()
