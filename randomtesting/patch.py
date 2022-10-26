class Patch:
    def __int__(self, status):
        self.status = status
        self.probability = 0

    def event(self):
        match self.status:
            case 1:
                self.status = 0
            case 2:
                self.status = 1
