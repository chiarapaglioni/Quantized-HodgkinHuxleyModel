import matplotlib.pyplot as plt


class IVplot:
    def __init__(self, v0, i0):
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.ax.set_xlim(-1, 2)
        self.ax.set_ylim(-7, 2)
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.v0 = v0
        self.i0 = i0
        self.xs = []
        self.ys = []
        self.dots, = self.ax.plot([], [], 'o', markersize=3)
        self.ax.set_xlabel('Voltage <V>')
        self.ax.set_ylabel('Current <I>')
        self.ax.set_title('IV Plot')

    def update(self, v, i):
        v = v / self.v0
        i = -i / self.i0
        self.xs.append(v)
        self.ys.append(-i)
        self.xs = self.xs[-2:]
        self.ys = self.ys[-2:]
        # Uncomment the next line if we want to see only one dot at each update
        # self.ax.cla()
        self.ax.set_xlim(-1, 2)
        self.ax.set_ylim(-7, 2)
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.plot(self.xs, self.ys, 'o', markersize=3)
        plt.pause(0.001)
