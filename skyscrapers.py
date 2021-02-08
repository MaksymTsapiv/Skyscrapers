"""skyscrapers"""


def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.
    """
    lines = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    return lines


def left_to_right_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.
    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.
    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    curr = input_line[1]
    counter = 1
    for j in input_line[2:-1]:
        if curr < j:
            curr = j
            counter += 1
    return counter == pivot


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.
    Return True if finished, False otherwise.
    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*',\
'*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*',\
'*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*',\
'*41532*', '*2*1***'])
    False
    """
    count = 0
    for string in board:
        if '?' in string:
            count += 1
    return count < 1


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.
    Return True if buildings in a row have unique length, False otherwise.
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*',\
'*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*',\
'*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*',\
'*41532*', '*2*1***'])
    False
    """
    count = 0
    for string in board[1:-1]:
        for digit in string[1:-1]:
            if string[1:-1].count(digit) > 1:
                count += 1
    return count < 1


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)
    Return True if all horizontal hints are satisfiable,
    i.e., for line 412453* , hint is 4, and 1245 are the four buildings
    that could be observed from the hint looking to the right.
    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*',\
'*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*',\
'*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*',\
'*41532*', '*2*1***'])
    False
    """
    result = True
    for i in board[1:-1]:
        if i[0] == i[-1] == '*':
            result &= True
        elif i[0] == '*' and i[-1] != '*':
            result &= left_to_right_check(i[::-1], int(i[-1]))
        elif i[0] != '*' and i[-1] != '*':
            result &= left_to_right_check(i, int(i[0]))
            result &= left_to_right_check(i[::-1], int(i[-1]))
        else:
            result &= left_to_right_check(i, int(i[0]))
    return result


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height)
    and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    result = [[None] * len(board) for _ in range(len(board[0]))]
    for i in range(len(board)):
        for j in range(len(board[0])):
            result[j][i] = board[i][j]
    for k in range(len(result)):
        result[k] = "".join(result[k])
    return check_horizontal_visibility(result) and check_uniqueness_in_rows(result)


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.
    """
    board = read_input(input_path)
    return check_not_finished_board(board) and check_uniqueness_in_rows(board)\
         and check_horizontal_visibility(board) and check_columns(board)

