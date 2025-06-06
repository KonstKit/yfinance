import random
from dataclasses import dataclass
from typing import List

@dataclass
class Cell:
    mine: bool = False
    revealed: bool = False
    flagged: bool = False
    adjacent: int = 0

class Minesweeper:
    def __init__(self, width: int = 9, height: int = 9, mines: int = 10):
        self.width = width
        self.height = height
        self.mines = mines
        self.board: List[List[Cell]] = [[Cell() for _ in range(width)] for _ in range(height)]
        self._place_mines()
        self._calculate_adjacency()
        self.lost = False

    def _place_mines(self):
        positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        for x, y in random.sample(positions, self.mines):
            self.board[y][x].mine = True

    def _calculate_adjacency(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x].mine:
                    continue
                count = 0
                for ny in range(max(0, y-1), min(self.height, y+2)):
                    for nx in range(max(0, x-1), min(self.width, x+2)):
                        if self.board[ny][nx].mine:
                            count += 1
                self.board[y][x].adjacent = count

    def display(self):
        print('   ' + ' '.join(f'{i}' for i in range(self.width)))
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = self.board[y][x]
                if cell.flagged:
                    row.append('F')
                elif not cell.revealed:
                    row.append('#')
                elif cell.mine:
                    row.append('*')
                elif cell.adjacent > 0:
                    row.append(str(cell.adjacent))
                else:
                    row.append(' ')
            print(f'{y:2} ' + ' '.join(row))

    def reveal(self, x: int, y: int):
        if not (0 <= x < self.width and 0 <= y < self.height):
            print('Coordinates out of range')
            return
        cell = self.board[y][x]
        if cell.revealed or cell.flagged:
            return
        cell.revealed = True
        if cell.mine:
            self.lost = True
            return
        if cell.adjacent == 0:
            for ny in range(max(0, y-1), min(self.height, y+2)):
                for nx in range(max(0, x-1), min(self.width, x+2)):
                    if not self.board[ny][nx].revealed:
                        self.reveal(nx, ny)

    def flag(self, x: int, y: int):
        if not (0 <= x < self.width and 0 <= y < self.height):
            print('Coordinates out of range')
            return
        cell = self.board[y][x]
        if cell.revealed:
            return
        cell.flagged = not cell.flagged

    def check_win(self) -> bool:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                if not cell.mine and not cell.revealed:
                    return False
        return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Play Minesweeper')
    parser.add_argument('--width', type=int, default=9)
    parser.add_argument('--height', type=int, default=9)
    parser.add_argument('--mines', type=int, default=10)
    args = parser.parse_args()

    game = Minesweeper(args.width, args.height, args.mines)

    while True:
        game.display()
        if game.lost:
            print('You hit a mine! Game over.')
            break
        if game.check_win():
            print('Congratulations! You cleared the minefield!')
            break
        cmd = input('Enter command (r x y to reveal, f x y to flag): ').split()
        if len(cmd) != 3:
            print('Invalid command')
            continue
        action, x_str, y_str = cmd
        if not (x_str.isdigit() and y_str.isdigit()):
            print('Invalid coordinates')
            continue
        x, y = int(x_str), int(y_str)
        if action == 'r':
            game.reveal(x, y)
        elif action == 'f':
            game.flag(x, y)
        else:
            print('Unknown action')

if __name__ == '__main__':
    main()
