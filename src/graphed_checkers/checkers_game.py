from .tile import Tile
from .graphics import GraphicCheckerBoard

def find_player_pieces(tile, player, piece_list):
    if tile.value == player:
        piece_list.append(tile.alias)


class CheckersGame:
    def __init__(self, board_configuration: int=1):
        self.checkerboard = Tile([0, 0]) if board_configuration == 1 else Tile([0, 1])
        self.prepare_checkerboard()
        self.graphic_checkerboard = GraphicCheckerBoard(self.checkerboard)
        self.graphic_checkerboard.update_board()

        self.player_pieces = []
        self.active_player = 1
        self.inactive_player = 2

        self.double_jump = False
        self.selected_tile = None
        self.possible_moves = {}
        self.move_selection = None

    def prepare_checkerboard(self):
        print('Building checkerboard...')
        self.checkerboard.build_checkerboard()

        print('Populating checkerboard...')
        self.checkerboard.populate_checkerboard()

    def play(self):
        while True:
            self.graphic_checkerboard.print_board()
            print(f'\n{"="*50}\n')
            print(f'Player {self.active_player}!')

            self.gameplay_loop()

            self.graphic_checkerboard.update_board()

            # Checking for win condition
            inactive_player_pieces = []
            self.checkerboard.traverse(self.inactive_player, inactive_player_pieces, tile_path={}, insert_function00=find_player_pieces)
            if not inactive_player_pieces:
                print(f'Congrats Player {self.active_player}! You won!')
                break

            self.active_player, self.inactive_player = self.inactive_player, self.active_player
            self.double_jump = False
            # self.reset_turn_values
            print('end of main loop.')

    def reset_turn_values(self):
        self.player_pieces = []

    def gameplay_loop(self):
        while True:
            self.present_player_pieces()
            self.select_piece()
            self.possible_moves = self.selected_tile.check_moves()
            self.present_possible_moves()
            if self.select_move():
                continue
            if self.selected_tile.move_piece(self.possible_moves[self.move_selection]) and not self.double_jump:
                self.double_jump_logic()
            break

            print('end of gameplay loop.')

    def double_jump_logic(self):
        self.selected_tile = self.checkerboard.traverse(tile_path={}, query_value=self.move_selection)
        self.possible_moves = self.selected_tile.check_moves()
        for move, instr in self.possible_moves.copy().items():
            if len(instr) < 2:
                del self.possible_moves[move]
        if not self.possible_moves:
            return False
        print('!!! DOUBLE JUMP !!!')
        self.double_jump = True
        self.present_possible_moves()
        self.select_move()
        self.selected_tile.move_piece(self.possible_moves[self.move_selection])

    def present_player_pieces(self):
        self.player_pieces = []
        print('\nYour pieces:')
        self.checkerboard.traverse(
            tile_path={},
            insert_function00=self.find_player_pieces
        )
        self.player_pieces.sort()
        for idx, piece in enumerate(self.player_pieces):
            print(f'{idx+1} | {piece}')

    def find_player_pieces(self, tile=None):
        if not tile:
            tile = self
        if tile.value == self.active_player:
            self.player_pieces.append(tile.alias)

    def select_piece(self):
        self.selected_tile = None
        while True:
            piece_selection = input('\nPlease select a piece: ')
            selected_tile = self.checkerboard.traverse(tile_path={}, query_value=piece_selection)

            if not selected_tile:
                print('*** Please choose a valid piece! ***')
                continue

            if piece_selection not in self.player_pieces:
                print('That\'s not your piece!')
                continue

            self.selected_tile = selected_tile
            break

    def present_possible_moves(self):
        print(f'Possible moves for {self.selected_tile.alias}:')
        for idx, move in enumerate(self.possible_moves):
            print(f'{idx+1} | {move}')
        if not self.possible_moves:
            print(f'No possible moves for {self.selected_tile.alias}.')

    def select_move(self):
        print(f'(Press [X] to return to piece selection)') if not self.double_jump \
            else f'(Press [X] to skip your double jump.)'

        repeat_flag = False
        while True:
            move_selection = input('Please select your move:')

            if move_selection.upper() == 'X':
                self.move_selection = None
                repeat_flag = True if not self.double_jump else False
                break
            elif move_selection not in self.possible_moves.keys():
                print('Please select a valid move!')
                continue
            break

        if repeat_flag:
            return True

        self.move_selection = move_selection
