import numpy as np

__author__ = 'def'


class RowIterator:
    def __init__(self, image):
        self.current_col = 0
        self.current_row = -1

        self.image = image
        self.cols = image.shape[0]
        self.rows = image.shape[1]

    def __iter__(self):
        return self

    def next(self):
        if self.current_row % 2 == 0: # Even row
            self.current_col += 1
            if self.current_col >= self.cols:
                self.current_row += 1
                self.current_col -= 1

        else: # Odd row
            self.current_col -= 1
            if self.current_col < 0:
                self.current_row += 1
                self.current_col += 1

        if self.current_row >= self.rows:
            raise StopIteration
        else:
            col = self.current_col
            row = self.current_row
            return (col , row), self.image[row, col]

def test_RowIterator():
    image = np.array([[0, 1, 2], [5, 4, 3], [6, 7, 8]])
    expected_values = range(9)
    values = []

    it = RowIterator(image)

    for (pos, px) in it:
        values.append(px)

    if len(values) == 0:
        raise  Exception("No pixels were returned")

    for a, b in zip( values, expected_values):
        if a != b:
            raise Exception("Test Failed: %d != %d" % (a, b))


if __name__ == '__main__':
    test_RowIterator()




