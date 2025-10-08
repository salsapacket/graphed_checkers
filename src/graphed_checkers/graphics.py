class GraphicCheckerBoard:
    def __init__(self, seed_tile, board_characters: list = ['-', 'X']):
        self.board_characters = board_characters
        self.seed_tile = seed_tile
        self.checker_board = self.generate_board()

    def generate_board(self):
        return [
            [
                (self.board_characters[0] if i % 2 == i2 % 2 else self.board_characters[1]) for i in range(0, 8)
            ]
            for i2 in range(0, 8)
        ]

    def update_board(self):
        self.seed_tile.traverse(tile_path={}, insert_function00=self.update_instructions)
        # traverse(self.seed_tile, tile_path={}, insert_function=self.update_instructions)

    def update_instructions(self, tile):
        tile_coordinate_transformed = [(7 - tile.coordinate[1]), (tile.coordinate[0])]
        if tile and tile.value:
            self.checker_board[tile_coordinate_transformed[0]][tile_coordinate_transformed[1]] = tile.value
        elif tile and not tile.value:
            self.checker_board[tile_coordinate_transformed[0]][tile_coordinate_transformed[1]] = \
             self.generate_board()[tile_coordinate_transformed[0]][tile_coordinate_transformed[1]]

    def print_board(self):
        for y_idx, y_val in enumerate(self.checker_board):
            print(f'{8-y_idx} | ', end='')
            for x_val in y_val:
                print(str(x_val)+' ', end='')
            print()
        print('  -----------------')
        print('    A B C D E F G H')
