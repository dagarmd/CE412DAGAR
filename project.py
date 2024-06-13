import simpy
import random
import matplotlib.pyplot as plt
import pandas as pd

# Constants
RANDOM_SEED = 12345
SIMULATION_TIME = 12000  # in minutes

# Define machine characteristics
machines_config = {
    'laser_cutting': {'count': 6, 'time': 14, 'breakdown_prob': 0.04, 'repair_time': 25},
    'assembly': {'count': 12, 'time': 17, 'breakdown_prob': 0.05, 'repair_time': 30},
    'painting': {'count': 8, 'time': 19, 'breakdown_prob': 0.06, 'repair_time': 40},
    'quality_control': {'count': 10, 'time': 8, 'breakdown_prob': 0.03, 'repair_time': 20},
    'packaging': {'count': 10, 'time': 10, 'breakdown_prob': 0.02, 'repair_time': 15}
}

# Define product characteristics
products_config = {
    'metal_frames': {'laser_cutting': 14, 'assembly': 17, 'painting': 19, 'quality_control': 8, 'packaging': 10},
    'wooden_toys': {'laser_cutting': 12, 'assembly': 20, 'painting': 18, 'quality_control': 10, 'packaging': 9},
    'plastic_containers': {'laser_cutting': 11, 'assembly': 15, 'painting': 20, 'quality_control': 7, 'packaging': 8},
    'electronic_modules': {'laser_cutting': 15, 'assembly': 18, 'painting': 21, 'quality_control': 9, 'packaging': 10},
    'glass_bottles': {'laser_cutting': 13, 'assembly': 16, 'painting': 17, 'quality_control': 8, 'packaging': 9}
}

class Machine:
    def __init__(self, env, name, count, time, breakdown_prob, repair_time, log, delays):
        self.env = env
        self.name = name
        self.machines = [simpy.Resource(env) for _ in range(count)]
        self.time = time
        self.breakdown_prob = breakdown_prob
        self.repair_time = repair_time
        self.log = log
        self.delays = delays

    def operate(self, index):
        while True:
            start_time = self.env.now
            yield self.env.timeout(self.time)
            self.log.append((self.env.now, f'{self.name} {index} completed an operation'))
            
            if random.random() < self.breakdown_prob:
                breakdown_time = self.env.now
                self.log.append((breakdown_time, f'{self.name} {index} broke down'))
                yield self.env.timeout(self.repair_time)
                repair_time = self.env.now
                self.log.append((repair_time, f'{self.name} {index} repaired'))
                self.delays.append((self.name, breakdown_time - start_time, repair_time - breakdown_time))

    def start(self):
        for i in range(len(self.machines)):
            self.env.process(self.operate(i))

def run_single_product_simulation():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    data = []
    log = []
    delays = []

    machines = [
        Machine(env, 'Laser Cutting', 6, 14, 0.04, 25, log, delays),
        Machine(env, 'Assembly', 12, 17, 0.05, 30, log, delays),
        Machine(env, 'Painting', 8, 19, 0.06, 40, log, delays),
        Machine(env, 'Quality Control', 10, 8, 0.03, 20, log, delays),
        Machine(env, 'Packaging', 10, 10, 0.02, 15, log, delays)
    ]

    for machine in machines:
        machine.start()

    def data_collector():
        while True:
            data.append((env.now, len(data)))
            yield env.timeout(60)

    env.process(data_collector())
    env.run(until=SIMULATION_TIME)
    return data, log, delays

def run_multi_product_simulation():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    data = []
    log = []
    delays = []

    machines = {
        'laser_cutting': Machine(env, 'Laser Cutting', 6, 14, 0.04, 25, log, delays),
        'assembly': Machine(env, 'Assembly', 12, 17, 0.05, 30, log, delays),
        'painting': Machine(env, 'Painting', 8, 19, 0.06, 40, log, delays),
        'quality_control': Machine(env, 'Quality Control', 10, 8, 0.03, 20, log, delays),
        'packaging': Machine(env, 'Packaging', 10, 10, 0.02, 15, log, delays)
    }

    products = [
        {'name': 'Metal Frames', 'operations': {'laser_cutting': 14, 'assembly': 17, 'painting': 19, 'quality_control': 8, 'packaging': 10}},
        {'name': 'Wooden Toys', 'operations': {'laser_cutting': 12, 'assembly': 20, 'painting': 18, 'quality_control': 10, 'packaging': 9}},
        {'name': 'Plastic Containers', 'operations': {'laser_cutting': 11, 'assembly': 15, 'painting': 20, 'quality_control': 7, 'packaging': 8}},
        {'name': 'Electronic Modules', 'operations': {'laser_cutting': 15, 'assembly': 18, 'painting': 21, 'quality_control': 9, 'packaging': 10}},
        {'name': 'Glass Bottles', 'operations': {'laser_cutting': 13, 'assembly': 16, 'painting': 17, 'quality_control': 8, 'packaging': 9}}
    ]

    for machine in machines.values():
        machine.start()

    def data_collector():
        while True:
            data.append((env.now, len(data)))
            yield env.timeout(60)

    env.process(data_collector())
    env.run(until=SIMULATION_TIME)
    return data, log, delays

data, log, delays = run_single_product_simulation()

df = pd.DataFrame(data, columns=['Time', 'Operations Completed'])
log_df = pd.DataFrame(log, columns=['Time', 'Event'])
delays_df = pd.DataFrame(delays, columns=['Machine', 'Operation Time', 'Repair Time'])
print("Single Product Line Simulation Data Summary:")
print(df.describe())

extended_data, extended_log, extended_delays = run_multi_product_simulation()

extended_df = pd.DataFrame(extended_data, columns=['Time', 'Operations Completed'])
extended_log_df = pd.DataFrame(extended_log, columns=['Time', 'Event'])
extended_delays_df = pd.DataFrame(extended_delays, columns=['Machine', 'Operation Time', 'Repair Time'])
print("\nMulti-product Line Simulation Data Summary:")
print(extended_df.describe())

def generate_report(log_df, delays_df, title):
    report = f"### {title} ###\n\n"
    report += "Event Counts:\n"
    report += log_df.groupby('Event').size().to_string() + '\n\n'
    report += "Delay Statistics:\n"
    report += delays_df.describe().to_string() + '\n\n'
    return report

single_product_report = generate_report(log_df, delays_df, "Single Product Line Simulation Report")
multi_product_report = generate_report(extended_log_df, extended_delays_df, "Multi-product Line Simulation Report")

print(single_product_report)
print(multi_product_report)

fig, axs = plt.subplots(3, 3, figsize=(18, 20))

axs[0, 0].plot(df['Time'], df['Operations Completed'], label='Operations completed over time')
axs[0, 0].set_title('Single Product Line Operations Over Time')
axs[0, 0].set_xlabel('Simulation Time (minutes)')
axs[0, 0].set_ylabel('Operations Completed')
axs[0, 0].legend()

axs[0, 1].plot(log_df['Time'], log_df.index, drawstyle='steps-post', label='Operations and Events')
axs[0, 1].set_title('Single Product Line Events')
axs[0, 1].set_xlabel('Simulation Time (minutes)')
axs[0, 1].set_ylabel('Event Count')
axs[0, 1].legend()

axs[0, 2].plot(extended_df['Time'], extended_df['Operations Completed'], label='Operations completed over time')
axs[0, 2].set_title('Multi-product Line Operations Over Time')
axs[0, 2].set_xlabel('Simulation Time (minutes)')
axs[0, 2].set_ylabel('Operations Completed')
axs[0, 2].legend()

axs[1, 0].plot(extended_log_df['Time'], extended_log_df.index, drawstyle='steps-post', label='Operations and Events')
axs[1, 0].set_title('Multi-product Line Events')
axs[1, 0].set_xlabel('Simulation Time (minutes)')
axs[1, 0].set_ylabel('Event Count')
axs[1, 0].legend()

delays_df.boxplot(column=['Operation Time', 'Repair Time'], ax=axs[1, 1])
axs[1, 1].set_title('Single Product Line Delay Statistics')
axs[1, 1].set_ylabel('Time (minutes)')

extended_delays_df.boxplot(column=['Operation Time', 'Repair Time'], ax=axs[1, 2])
axs[1, 2].set_title('Multi-product Line Delay Statistics')
axs[1, 2].set_ylabel('Time (minutes)')

delays_df.hist(column='Operation Time', bins=20, ax=axs[2, 0])
axs[2, 0].set_title('Single Product Line Operation Time Distribution')
axs[2, 0].set_xlabel('Operation Time (minutes)')
axs[2, 0].set_ylabel('Frequency')

delays_df.hist(column='Repair Time', bins=20, ax=axs[2, 1])
axs[2, 1].set_title('Single Product Line Repair Time Distribution')
axs[2, 1].set_xlabel('Repair Time (minutes)')
axs[2, 1].set_ylabel('Frequency')

extended_delays_df.hist(column='Operation Time', bins=20, ax=axs[2, 2])
axs[2, 2].set_title('Multi-product Line Operation Time Distribution')
axs[2, 2].set_xlabel('Operation Time (minutes)')
axs[2, 2].set_ylabel('Frequency')

plt.tight_layout()
plt.show()
