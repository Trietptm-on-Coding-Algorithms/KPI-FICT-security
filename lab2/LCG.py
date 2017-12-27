A = 1664525
C = 1013904223
M = 4294967296


class LCG:
    def __init__(self, initial_state):
        self.current = initial_state

    def print_state(self):
        print(self.current)

    def extract_number(self):
        self.current = (A * self.current + C) % M
        if self.current > 2147483648:
            self.current = self.current - 4294967296
        return self.current
