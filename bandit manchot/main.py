import matplotlib.pyplot as plt
""" a relirs exo3 au point 1 """

from bandit import Bandit


def main():
    bandit = Bandit()
    rewards = [bandit.play() for _ in range(1000)]

    plt.hist(rewards, bins=40, density=True, alpha=0.6, edgecolor="black")
    plt.axvline(bandit.avg, color="red", linestyle="--", label="avg")
    plt.xlabel("Récompense")
    plt.ylabel("Densité")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
