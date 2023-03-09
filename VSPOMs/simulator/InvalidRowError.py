class InvalidRowError(Exception):
    def __int__(self, item, column, line_number, row):
        super().__init__("fart")
        self.item = item
        self.column = column
        self.line_number = line_number
        self.row = row

    # def __str__(self):
    #     message = f"item: {self.item} at column {self.column}, on line {self.line_number}, full row:\n{self.row}"
    #     message = "poo"
    #     return message
