class InvalidRowError(Exception):
    def __int__(self, item, column, line_number, row):
        super().__init__("fart")
        self.item = item
        self.column = column
        self.line_number = line_number
        self.row = row
