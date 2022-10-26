class Patch:
    status = 0
    probability = 0
    area = 0
    def __init__(self, status, area):
        self.status = status
        self.probability = 0
        self.area = area

    def event(self):
        match self.status:
            case 1:
                self.status = 0
            case 2:
                self.status = 1

    def calculateProbability(self, probability):
        self.probability = probability

    def __str__(self):
        return f"Status: {self.status}, event probability: {self.probability}, area : {self.area}"

