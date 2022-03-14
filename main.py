from __future__ import annotations

import itertools
from typing import Optional, NoReturn

from pysat.solvers import Solver


def coordinates_to_number(x: int, y: int, field_size: int) -> int:
    return x * field_size + y + 1


def number_to_coordinates(number: int, field_size: int) -> tuple[int, int]:
    zero_based_number = number - 1
    return zero_based_number // field_size, zero_based_number % field_size


def get_cnf_threatened_cells(x: int, y: int, field_size: int) -> list[list[int]]:
    cnf = []
    for dx, dy in itertools.product([-1, 0, 1], repeat=2):
        if dx == 0 and dy == 0:
            continue

        for i in range(1, field_size + 1):
            new_x = x + dx * i
            new_y = y + dy * i
            if not (0 <= new_x < field_size and 0 <= new_y < field_size):
                break
            cnf.append([-coordinates_to_number(x, y, field_size), -coordinates_to_number(new_x, new_y, field_size)])
    return cnf


def get_eight_queens_puzzle_cnf(field_size: int) -> Optional[list[list[int]]]:
    cnf_n_queens_must_be_present = [
        [coordinates_to_number(x, y, field_size) for y in range(field_size)] for x in range(field_size)
    ]
    cnf_queen_threatens_queen = list(itertools.chain.from_iterable([
        get_cnf_threatened_cells(x, y, field_size) for x, y in itertools.product(range(field_size), repeat=2)
    ]))

    return cnf_n_queens_must_be_present + cnf_queen_threatens_queen


def solve_sat(cnf: Optional[list[list[int]]]) -> list[int]:
    with Solver(bootstrap_with=cnf) as solver:
        solver.solve()
        return solver.get_model()


def print_solution(solution: Optional[list[int]], field_size: int) -> NoReturn:
    if solution is None:
        print('No solution!')
        return

    print('"*" - queen, "." - empty cell')
    field = [['.'] * field_size for _ in range(field_size)]
    for variable in solution:
        if variable > 0:
            x, y = number_to_coordinates(variable, field_size)
            field[x][y] = '*'

    for row in field:
        print(''.join(row))


if __name__ == '__main__':
    n = int(input('Number of queens: '))
    eight_queens_puzzle_cnf = get_eight_queens_puzzle_cnf(n)
    cnf_solution = solve_sat(eight_queens_puzzle_cnf)
    print_solution(cnf_solution, n)
