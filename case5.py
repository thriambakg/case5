import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from scipy import stats

class Task:
    def __init__(self, name, min_duration, most_likely_duration, max_duration, cost_per_week):
        self.name = name
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.most_likely_duration = most_likely_duration
        self.cost_per_week = cost_per_week
        self.predecessor = []
        self.start_date = None

    def set_start_date(self,start_date):
        self.start_date = start_date

    def set_predecessor(self, predecessor_task):
        self.predecessor.append(predecessor_task)

    def get_predecessor(self):
        return self.predecessor

    def calculate_duration(self):
        return np.random.triangular(self.min_duration, self.most_likely_duration, self.max_duration)

    def calculate_cost(self):
        return (self.calculate_duration() / 7) * self.cost_per_week

def calculate(start_task, end_task):
    visited = set()
    stack = [end_task]
    total_duration = 0
    total_cost = 0

    while stack:
        current_task = stack.pop()
        #print(f"current task: {current_task.name}")
        if current_task in visited:
            continue
        visited.add(current_task)
        total_duration += current_task.calculate_duration()
        total_cost += current_task.cost_per_week

        if current_task == start_task:
            break
        

        largest_predecessor = None
        largest_predecessor_duration = -1
        for predecessor in current_task.predecessor:
            if predecessor not in visited:
                predecessor_duration = predecessor.calculate_duration()
                if predecessor_duration > largest_predecessor_duration:
                    largest_predecessor = predecessor
                    largest_predecessor_duration = predecessor_duration

        if largest_predecessor is not None:
            stack.append(largest_predecessor)

    return total_duration, total_cost

def main():
    
    task_1 = Task("Installation of 900 thermal blankets", 25, 42.0, 98, cost_per_week=19200)
    task_2 = Task("Cryovacuum test", 93, 110.0, 145, cost_per_week=17500)
    task_3 = Task("Update test cooling chamber processes", 60, 75.0, 110, cost_per_week=8600)
    task_4 = Task("Optical ground support equipment test 1", 115, 135.0, 160, cost_per_week=12600)
    task_5 = Task("Optical ground support equipment test 2", 80, 96.0, 135, cost_per_week=14400)
    task_6 = Task("Thermal Pathfinder Test", 140, 170.0, 220, cost_per_week=18100)
    task_7 = Task("Instrument integration and test", 180, 225.0, 280, cost_per_week=7800)
    task_8 = Task("Telescope Integration and Test", 210, 250.0, 310, cost_per_week=11000)
    task_9 = Task("Modification of OTE", 60, 80, 140, cost_per_week=8650)
    task_10 = Task("Modification of ground support equipment", 90, 120, 165, cost_per_week=7970)

    
    task_4.set_start_date(dt.date(2015,1,5))
    task_7.set_start_date(dt.date(2015,1,15))
    task_8.set_start_date(dt.date(2015,4,3))

    task_1.set_predecessor(task_7)
    task_1.set_predecessor(task_8)
    task_2.set_predecessor(task_6)
    task_2.set_predecessor(task_1)
    task_3.set_predecessor(task_5)
    task_5.set_predecessor(task_4)
    task_6.set_predecessor(task_3)
    task_6.set_predecessor(task_9)
    task_6.set_predecessor(task_10)
    task_9.set_predecessor(task_5)
    task_10.set_predecessor(task_5)



    total_durations = []
    total_costs = []
    for _ in range(10000):
        total_duration, total_cost = calculate(task_4, task_2)
        total_durations.append(total_duration)
        total_costs.append(total_cost)

    # Create histograms
    fig, axs = plt.subplots(2)
    axs[0].hist(total_durations, bins=50, alpha=0.75, color='b', edgecolor='black')
    axs[0].set_title('Total Estimated Duration')
    axs[0].set_xlabel('Duration (days)')
    axs[0].set_ylabel('Frequency')
    axs[1].hist(total_costs, bins=50, alpha=0.75, color='r', edgecolor='black')
    axs[1].set_title('Total Cost')
    axs[1].set_xlabel('Cost ($)')
    axs[1].set_ylabel('Frequency')

    # Calculate mean, median, and standard deviation
    mean_duration = np.mean(total_durations)
    median_duration = np.median(total_durations)
    std_duration = np.std(total_durations)

    mean_cost = np.mean(total_costs)
    median_cost = np.median(total_costs)
    std_cost = np.std(total_costs)

    conf_interval_duration = stats.norm.interval(0.95, loc=mean_duration, scale=std_duration/np.sqrt(len(total_durations)))
    conf_interval_cost = stats.norm.interval(0.95, loc=mean_cost, scale=std_cost/np.sqrt(len(total_costs)))

    print(f"Total Estimated Duration - Mean: {mean_duration},Median: {median_duration}, St. Dev: {std_duration}, 95% CI: {conf_interval_duration}")
    print(f"Total Cost - Mean: {mean_cost}, Median: {median_cost}, St. Dev: {std_cost}, 95% CI: {conf_interval_cost}")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
