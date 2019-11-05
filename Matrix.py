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

        print(left_string + '\n' + top_string)
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

        # Take care of initializing the blank spaces in the lower right diagonal region of array
        max_blanks = 3
        current_num_blanks = 3
        row = self.rows - 1
        for i in range(max_blanks):
            col = self.bandwidth - 1
            while current_num_blanks != 0:
                self.array[row][col] = None
                current_num_blanks -= 1
                col -= 1
            row -= 1
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


