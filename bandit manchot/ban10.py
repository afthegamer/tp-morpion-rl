from bandit import Bandit

class Ban10:
    def __init__(self):
        self.bandits = [Bandit() for _ in range(10)]
        self.best = max(range(10), key=lambda i: self.bandits[i].avg)

    def play(self, arm):
        if not 0 <= arm < 10:
            raise ValueError("Arm must be between 0 and 9")
        return self.bandits[arm].play()