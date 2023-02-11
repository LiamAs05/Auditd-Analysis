import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from DBManager import Actions


class Visualizer:

    @staticmethod
    def visualize(syscalls: list[str]) -> None:
        """
        This functions creates a pie chart that shows the distribution of the syscalls made in the system.
        @param syscalls list of all syscalls in the log file
        @return None
        """ 
        labels = 'fork', 'kill', 'chdir', 'execve'
        sizes = [0, 0, 0, 0]
        for syscall in syscalls:
            for label in labels:
                if syscall == label:
                    sizes[labels.index(label)] += 1
                    break

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()
