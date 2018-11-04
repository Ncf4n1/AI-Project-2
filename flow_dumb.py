def init_maze():
    with open('5x5.txt') as file:
        lines = file.read().strip().splitlines()

    return lines


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

def backtrack(maze):
    start = find_start(maze)

    print(start)



def main():
    maze = init_maze()

    backtrack(maze)

main()
