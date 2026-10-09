class GreedyPlayer:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.counts = [0] * n_arms  # Number of times each arm has been played
        self.values = [0.0] * n_arms  # Estimated value of each arm

    def select_arm(self):
        # Select the arm with the highest estimated value
        return self.values.index(max(self.values))

    def update(self, chosen_arm, reward):
        # Update the counts and estimated values for the chosen arm
        self.counts[chosen_arm] += 1
        n = self.counts[chosen_arm]
        value = self.values[chosen_arm]
        # Update the estimated value using incremental formula
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[chosen_arm] = new_value