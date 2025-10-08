class Tile:
    checkerboard_x_bound = 7
    checkerboard_y_bound = 7

    def __init__(
            self,
            coordinate,
            value=None
    ):
        self.value = value
        self.is_king = False
        self.coordinate = coordinate
        self.upper_left = None
        self.upper_right = None
        self.lower_left = None
        self.lower_right = None
        self.create_coordinate_alias()
        self.possible_moves = self.check_moves()
        # self.possible_moves =

    def create_coordinate_alias(self):
        alpha_num_map = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        coordinate_alias = f'{alpha_num_map[self.coordinate[0]]}{self.coordinate[1]+1}'
        self.alias = coordinate_alias

    def build_checkerboard(self, tile=None, tile_path: dict={}):
        if not tile:
            tile = self
        tile_path[tile.alias] = tile

        def make_tile(coord_delta, direction, opposite):
            new_coordinate = [tile.coordinate[0] + coord_delta[0], tile.coordinate[1] + coord_delta[1]]
            if (new_coordinate[0] < 0 or self.checkerboard_x_bound < new_coordinate[0]) \
                    or (new_coordinate[1] < 0 or self.checkerboard_y_bound < new_coordinate[1]):
                return False

            new_tile = Tile(new_coordinate)

            if new_tile.alias in tile_path:
                setattr(tile, direction, tile_path[new_tile.alias])
                return False

            setattr(tile, direction, new_tile)
            setattr(new_tile, opposite, tile)
            self.build_checkerboard(tile=new_tile, tile_path=tile_path)

        make_tile([1, 1], 'upper_right', 'lower_left')
        make_tile([1, -1], 'lower_right', 'upper_left')
        make_tile([-1, -1], 'lower_left', 'upper_right')
        make_tile([-1, 1], 'upper_left', 'lower_right')
        return

    def traverse(
            self,
            *args,
            tile=None,
            tile_path={},
            insert_function00=None,
            insert_function01=None, # This is here for future expansion into the 'go' function
            query_value=None
    ):
        def go(direction):
            new_tile = getattr(tile, direction)
            if not new_tile:
                return False
            if new_tile.alias in tile_path:
                return False

            return self.traverse(
                *args,
                tile=new_tile,
                tile_path=tile_path,
                insert_function00=insert_function00,
                query_value=query_value
            )

        if not tile:
            tile = self

        tile_path[tile.alias] = tile

        if insert_function00:
            insert_function00(tile, *args)

        if query_value:
            if tile.alias == query_value:
                return tile

        for _direction in ['upper_right', 'lower_right', 'lower_left', 'upper_left']:
            result = go(_direction)
            if result:
                return result
        return

    def populate_checkerboard(self):
        self.traverse(tile_path={}, insert_function00=self.populate_checkerboard_instructions)

    def populate_checkerboard_instructions(self, tile):
        if tile.coordinate[1] < 3:
            tile.value = 1
        elif tile.coordinate[1] > 4:
            tile.value = 2

    def check_moves(self):
        possible_moves = {}

        if self.is_king:
            viable_directions = ['upper_right', 'upper_left', 'lower_right', 'lower_left']
        elif self.value == 1:
            viable_directions = ['upper_right', 'upper_left']
        elif self.value == 2:
            viable_directions = ['lower_right', 'lower_left']
        else:
            viable_directions = []

        for direction in viable_directions:
            next_tile = getattr(self, direction)
            if not next_tile:
                continue
            if not next_tile.value:
                possible_moves[next_tile.alias] = [direction]
                continue
            if next_tile.value != self.value:
                hop_tile = getattr(next_tile, direction)
                if not hop_tile:
                    continue
                if not hop_tile.value:
                    possible_moves[hop_tile.alias] = [direction, direction]
        return possible_moves

    def move_piece(self, move_instructions):
        player = self.value
        tile = self
        for instr in move_instructions:
            tile.value = None
            tile = getattr(tile, instr)
        tile.is_king = True if self.is_king else False
        tile.value = player

        if (tile.coordinate[1] == 7 and tile.value == 1) or (tile.coordinate[1] == 0 and tile.value == 2):
            print('King me!')
            tile.is_king = True
        # Returns True to indicate it is eligible for double jump
        if len(move_instructions) > 1 and tile.check_moves():
            return True
