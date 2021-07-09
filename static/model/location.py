class location:
    def __init__(self):
        self.locations = []
        self.locations = {
        "corridor1" : 0,
        "corridor2" : 1,
        "lab1" : 2,
        "lab2" : 3,
        "lab3" : 4,
        "cafe1" : '192.168.0.11:8080/video',
        "cafe2" :'192.168.0.31:8080/video',
        "GateIn" : '192.168.0.14:8080/video',
        "GateOut" : '192.168.0.21:8080/video',
        }

    def getLocation(self):
        return self.locations
    