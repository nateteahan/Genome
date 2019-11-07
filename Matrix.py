class Matrix:
    def __init__(self, sequence_one, sequence_two):
        self.rows = len(sequence_two) + 1
        self.cols = len(sequence_one) + 1
        self.top_sequence = sequence_one
        self.left_sequence = sequence_two
        self.array = [[0 for i in range(self.cols)] for j in range(self.rows)]
        self.previous = [["" for i in range(self.cols)] for j in range(self.rows)]

        # print ("evaluating " + self.top_sequence + " and " + self.left_sequence)

        # Initialize the first column to multiples of 5
        total_sum = 0
        for i in range(self.rows):
            self.array[i][0] = total_sum
            total_sum += 5

        # Initialize the first row to multiples of 5
        total_sum = 5
        for i in range(1, self.cols):
            self.array[0][i] = total_sum
            total_sum += 5

    def get_left(self, row, col):
        return self.array[row][col - 1]

    def get_above(self, row, col):
        return self.array[row - 1][col]

    def get_diagonal(self, row, col):
        return self.array[row - 1][col - 1]

    # Handles tie breaking
    def get_minimum(self, left, top, diagonal):
        # In the case of a tie, min function returns the first one in the list of parameters
        minimum_value = min(left, top, diagonal)

        if minimum_value == left:
            return left, "left"

        if minimum_value == top:
            return top, "top"

        return diagonal, "diagonal"

    def determine_match(self, row, col):
        if self.left_sequence[row - 1] == self.top_sequence[col - 1]:
            return True
        return False

    def compute_alignment(self):
        for i in range(1, self.rows):
            for j in range(1, self.cols):
                score, neighbor = self.compute_element(i, j)
                self.array[i][j] = score
                self.previous[i][j] = neighbor

        return self.compute_string_alignments()

    def get_final_score(self):
        return self.array[-1][-1]

    def compute_element(self, row, col):
        if self.determine_match(row, col):
            diagonal_cost = self.get_diagonal(row, col) - 3
        else:
            diagonal_cost = self.get_diagonal(row, col) + 1

        left_cost = self.get_left(row, col) + 5
        above_cost = self.get_above(row, col) + 5

        # returns a score and where it came from
        return self.get_minimum(left_cost, above_cost, diagonal_cost)

    def compute_string_alignments(self):
        # Start at the bottom right corner of the array and work back up
        row = self.rows - 1
        column = self.cols - 1
        current = self.previous[row][column]

        left_string = self.left_sequence
        top_string = self.top_sequence

        while current is not "":
            if current == "diagonal":
                row -= 1
                column -= 1

            if current == "top":
                top_string = top_string[:column] + '-' + top_string[column:]
                row = row - 1

            if current == "left":
                left_string = left_string[:row] + '-' + left_string[row:]
                column = column - 1

            current = self.previous[row][column]

        while row != 0:
            top_string = top_string[:column] + '-' + top_string[column:]
            row -= 1
        while column != 0:
            left_string = left_string[:row] + '-' + left_string[row:]
            column -= 1

        # print(left_string + '\n' + top_string)
        return left_string, top_string


class Restricted:
    def __init__(self, sequence_one, sequence_two):
        # n equals the size of the largest string
        if len(sequence_one) > len(sequence_two):
            self.rows = len(sequence_one) + 1
        else:
            self.rows = len(sequence_two) + 1

        self.bandwidth = 7
        self.top_sequence = sequence_one
        self.left_sequence = sequence_two
        self.array = [[0 for i in range(self.bandwidth)] for j in range(self.rows)]
        self.previous = [["" for i in range(self.bandwidth)] for j in range(self.rows)]

        # Take care of initializing the blank spaces in the upper left diagonal region of array
        max_blanks = 3
        current_num_blanks = 3
        row = 0
        for i in range(max_blanks):
            col = 0
            while current_num_blanks != 0:
                self.array[row][col] = None
                current_num_blanks -= 1
                col += 1
            row += 1
            max_blanks -= 1
            current_num_blanks = max_blanks

        # Take care of initializing the base case values in the array
        self.initialize_base()

    def initialize_base(self):
        row = 0
        col = 3

        # Handle first row base case
        _sum = 0
        for col in range(self.bandwidth):
            if self.array[row][col] is not None:
                self.array[row][col] = _sum
                _sum += 5

        row += 1
        col = 0
        _sum = 5
        while row != 4:
            while self.array[row][col] is None:
                col += 1
            self.array[row][col] = _sum
            _sum += 5
            row += 1
            col = 0

        return

    def get_left(self, row, col):
        if col < 1:
            return float("inf")

        if self.array[row][col - 1] is None:
            return float("inf")

        return self.array[row][col - 1]

    def get_above(self, row, col):
        if row < 1 or col == self.bandwidth - 1:
            return float("inf")

        # returning infinity so that I can still use it for the get_minimum function
        if self.array[row - 1][col + 1] is None:
            return float("inf")

        return self.array[row - 1][col + 1]

    def get_diagonal(self, row, col):
        if row < 1:
            return float("inf")

        if self.array[row - 1][col] is None:
            return float("inf")

        return self.array[row - 1][col]

    def compute_element(self, row, col):
        index = self.get_index(row, col)

        # problem is passing in index instead of column..
        if self.determine_match(row, index):
            diagonal = self.get_diagonal(row, col) - 3
        else:
            diagonal = self.get_diagonal(row, col) + 1

        left = self.get_left(row, col) + 5
        above = self.get_above(row, col) + 5

        return self.get_minimum(left, above, diagonal)

    def get_index(self, row, col):
        # 3 is the last row of the base case val.
        # row - 3 returns how far down the band we are from the last base value 15
        # + col just makes sure that we get the right index as we move across the row
        # Important to do this step in parts. For all the values up to row 3 (0-3), since they haven't been shifted
        # then the ones after since they have been shifted

        # Check for unshifted rows
        # the col - x is simply the number of null values are at the end of the row that need to be subtracted
        # to get the proper index
        if row <= 3:
            if row == 0:
                return col - 3
            if row == 1:
                return col - 2
            if row == 2:
                return col - 1
            else:
                return col
        else:
            return (row - 3) + col

    def get_minimum(self, left, top, diagonal):
        min_value = min(left, top, diagonal)

        if min_value == left:
            return left, "left"
        if min_value == top:
            return top, "top"

        return diagonal, "diagonal"

    def determine_match(self, row, col):
        # Need to subtract one because we are taking the '-' character into account
        if self.left_sequence[row - 1] == self.top_sequence[col - 1]:
            return True
        else:
            return False

    def compute_string_alignments(self):
        # Start at the bottom right corner of the array and work back up
        row = self.rows - 1
        column = self.get_score_column()

        current = self.previous[row][column]
        left_string = self.left_sequence
        top_string = self.top_sequence
        while current is not "":
            if current == "diagonal":
                # banded algorithm means value is just up a row
                row -= 1

            if current == "top":
                # banded algorithm means value is up a row and to the right
                top_string = top_string[:column] + '-' + top_string[column:]
                row = row - 1
                column += 1

            if current == "left":
                # banded algorithm is the same for left values
                left_string = left_string[:row] + '-' + left_string[row:]
                column = column - 1

            current = self.previous[row][column]

        while row != 0:
            top_string = top_string[:column] + '-' + top_string[column:]
            row -= 1
        while column > 3:
            left_string = left_string[:row] + '-' + left_string[row:]
            column -= 1

        print(left_string + '\n' + top_string)

        return left_string, top_string

    def get_score_column(self):
        # Finds the column with the first non-None value in the final row of the array. This is the total score
        final_row = self.rows - 1
        final_column = self.bandwidth - 1
        total_score = self.array[final_row][final_column]

        count = 0
        while total_score is None:
            count += 1
            total_score = self.array[final_row][final_column - count]

        return final_column - count

    def get_final_score(self):
        index = self.get_score_column()

        return self.array[self.rows - 1][index]

    def compute_alignment(self):
        for i in range(1, self.rows):
            for j in range(self.bandwidth):
                # Keeps track of the bandwidth width for each row and location in it
                boundary_check = self.get_index(i, j)

                if self.array[i][j] is not None:
                    if boundary_check > len(self.top_sequence):
                        self.array[i][j] = None
                    else:
                        score, neighbor = self.compute_element(i, j)
                        self.array[i][j] = score
                        self.previous[i][j] = neighbor

        return self.compute_string_alignments()
