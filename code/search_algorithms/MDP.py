from search_algorithms.BaseSearch import BaseSearch


class MDP(BaseSearch):
    """
    Skeleton for MDP-based maze solving with Value Iteration and Policy Iteration.
    """

    def __init__(self, gamma=0.9, theta=1e-6, step_reward=-1.0, goal_reward=0.0):
        super().__init__()
        self.gamma = gamma
        self.theta = theta
        self.step_reward = step_reward
        self.goal_reward = goal_reward

    def solve(self, maze, start, goal, on_expand=None):
        print("In solve")
        print(maze)
        print(start)
        print(goal)
