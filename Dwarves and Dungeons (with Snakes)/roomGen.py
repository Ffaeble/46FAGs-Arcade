import random as rng
from Testing.oreGen import oreMap
"""
Code may or may not have been influenced by:
Divine intervention
Aliens
Cosmic Rays
and Puppys and kittens
"""

def create_room(width, height):
    """Create a 2D list representation of a room."""
    return [['░'] * height for _ in range(width)]


def place_rooms(max_x, max_y, room_count, board):
    """Place random rooms on the board."""
    for _ in range(room_count):
        min_size, max_size = 2, 6
        room_x, room_y = rng.randint(0, max_x - 1), rng.randint(0, max_y - 1)
        room_width, room_height = rng.randint(min_size, max_size), rng.randint(min_size, max_size)
        room = create_room(room_width, room_height)
        for x in range(room_width):
            for y in range(room_height):
                if room_x + x < max_x and room_y + y < max_y:
                    board[room_x + x][room_y + y] = room[x][y]


def empty_borders(board, max_x, max_y):
    """Empty the border tiles around the board."""
    for x in range(max_x):
        board[x][0] = board[x][max_y - 1] = '▓'
    for y in range(max_y):
        board[0][y] = board[max_x - 1][y] = '▓'
    return place_walls(board, max_x, max_y)


def fdup_magic(dir_byte):
    directions = [(dir_byte >> i) & 1 for i in range(8)]
    south_east, south, south_west, east, west, north_east, north, north_west = directions

    edge_mask = 0x5a
    corner_mask = 0xa5

    edge_sum = bin(dir_byte & edge_mask).count('1')
    corner_sum = bin(dir_byte & corner_mask).count('1')

    if edge_sum == 4:
        return 'O'
    elif edge_sum == 3:
        return '═' if not (west & east) else '║'
    elif edge_sum == 2:
        corner_edges = [
            ((west & east), '║'),
            ((north & south), '═'),
            ((south & east), '╝'),
            ((south & west), '╚'),
            ((north & east), '╗'),
            ((north & west), '╔')
        ]
        return next(symbol for case, symbol in corner_edges if case)
    elif edge_sum == 1:
        if corner_sum == 0:
            return '═' if (north | south) else '║'
        elif corner_sum >= 1:
            t_edges = [
                (north & (south_east | south_west), '╦'),
                (south & (north_east | north_west), '╩'),
                (west & (north_east | south_east), '╠'),
                (east & (north_west | south_west), '╣'),
                (north | south, '═'),
                (west | east, '║')
            ]
            return next(symbol for case, symbol in t_edges if case)
    elif edge_sum == 0:
        if corner_sum == 1:
            corners = [south_east, south_west, north_east, north_west]
            return ['╔', '╗', '╚', '╝'][corners.index(1)]
        elif corner_sum >= 2:
            if (north_west & south_east) or (north_east & south_west):
                return '╬'
            t_pairs = [
                (north_west & north_east, '╩'),
                (south_west & south_east, '╦'),
                (north_west & south_west, '╣'),
                (north_east & south_east, '╠')
            ]
            return next(symbol for pair, symbol in t_pairs if pair)


def place_walls(board, max_x, max_y):
    """Place walls around the rooms."""
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for x in range(max_x):
        for y in range(max_y):
            dir_byte = 0
            for i, (dx, dy) in enumerate(directions):
                nx, ny = x + dx, y + dy
                if (
                    nx < 0 or nx >= max_x or
                    ny < 0 or ny >= max_y or
                    board[nx][ny] == '░'
                ):
                    dir_byte |= (1 << (7 - i))

            if board[x][y] == '▓' and dir_byte:
                board[x][y] = fdup_magic(dir_byte)

    return board


def map_init():
    """Initialize the map."""
    max_x, max_y = 48, 235
    room_count = rng.randint(1, 400)
    board = [['▓'] * max_y for _ in range(max_x)]

    place_rooms(max_x, max_y, room_count, board)
    return empty_borders(board, max_x, max_y)

def prntMap (board):
    reset = "\033[0m"
    oreMapD = oreMap(48, 235)
    for x in range(48):
        for y in range(235):
            board[x][y] = oreMapD[x][y] + board[x][y] + reset 
    for row in board:
        print(''.join(row))

def resetprint():
    lines = 48
    print("\33[F"*lines, end='')
    for i in range(lines):
        print()
          

def main():
    """Main function."""
    board = map_init()
    return(board)
