class Patch:
    def __int__(self, status, area):
        self.status = status
        self.area = area
        self.probability = 0

    def event(self):
        match self.status:
            case 1:
                self.status = 0
            case 2:
                self.status = 1
