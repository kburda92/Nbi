class Net:
    def __init__(self, _node = 0):
        self.node = _node
        self.degree = 0
        self.neighbor = []
        self.value = 0.0

    def __lt__(self, other):
        return self.node < other.node