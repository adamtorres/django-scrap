class Table(list):
    """
    Attempts to make formatting a table on the console easier by handling the padding.
    Add lists to the Table via append or extend as it is a list itself.
    Call `print` to have Table print the data.
    Call `to_string` to get the string which `print` would use.
    Call `row_to_string` to get a generator which would result in the list `to_string` would produce.

        >>> x = table.Table()
        >>> x.default_alignment = '^'
        >>> x.append(['a', 'b', 'ccccc'])
        >>> x.append(['a', 'bbb','c', 'dd'])
        >>> print(x)
        [['a', 'b', 'ccccc'], ['a', 'bbb', 'c', 'dd']]
        >>> x.print()
        a |  b  | ccccc |
        a | bbb |   c   | dd
        >>> print(x)  # To show the lists have not been modified
        [['a', 'b', 'ccccc'], ['a', 'bbb', 'c', 'dd']]
    """
    max_lens = []
    formatting = []
    default_alignment = ">"

    def __init__(self):
        super().__init__()

    def append(self, row):
        super().append(row)
        self.check_max_lens(row)

    def check_max_lens(self, row):
        """
        Keeps the max_lens list updated by making sure it covers all of the values in the new row.
        """
        while len(row) > len(self.max_lens):
            self.max_lens.append(0)
            self.formatting.append(self.default_alignment)
        for i, cell in enumerate(row):
            if len(cell) > self.max_lens[i]:
                self.max_lens[i] = len(cell)

    def extend(self, rows):
        """
        This does not call self.append for each item in rows.
        """
        super().extend(rows)
        # list(map(self.check_max_lens, rows))
        for row in rows:
            self.check_max_lens(row)

    def print(self):
        """
        Print the contents of the Table.
        """
        print(self.to_string())

    def row_to_string(self):
        """
        Convert and yield each row to a string applying the max length so all columns line up in a fixed-width font.
        Does not modify the stored lists as it makes a copy when needed.
        """
        format_string = " | ".join(f"{{{i}:{self.formatting[i]}{max_len}}}" for i, max_len in enumerate(self.max_lens))
        for row in self:
            tmp_row = row[:]
            while len(tmp_row) < len(self.max_lens):
                tmp_row.append("")
            yield format_string.format(*tmp_row)

    def to_string(self):
        """
        Convert the Table to a string.
        """
        return "\n".join(self.row_to_string())
