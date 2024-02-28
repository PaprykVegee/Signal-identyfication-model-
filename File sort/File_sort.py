import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from test_module import SortFile
from signal_to_tf import signal_to_tf

class AppToTest(SortFile):
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x500")

        # Open file button
        open_file_button = tk.Button(self.master, text="open file", command=self.file_open)
        open_file_button.place(x=30, y=30)

        # Execute button
        execute_button = tk.Button(self.master, text="Execute", command=self.execute)
        execute_button.place(x=100, y=30)

        # Plot button
        # plot_button = tk.Button(self.master, text="Plot", command=self.plot_graph)
        # plot_button.place(x=170, y=30)

        # Clear data
        clear_button = tk.Button(self.master, text="Clear", command=self.clear)
        clear_button.place(x=30, y=60)


        # Initialize a figure and axis for plotting
        self.fig, (self.ax, self.ax_domein, self.ax_dft) = plt.subplots(nrows=3)
        # self.ax.set_aspect('equal', 'box')

        self.list_box = tk.Listbox(self.master)
        self.list_box.place(x=300, y=30)

    def clear(self):
        self.ax.clear()
        self.ax_domein.clear()
        self.ax_dft.clear()
        self.canvas.draw()
        self.list_box.delete(0, tk.END)
        del self.filepaths

    def file_open(self):
        self.filepaths = filedialog.askopenfilenames(initialdir="/", title="Wybierz Plik", filetypes=(("Pliki tekstowe", ".txt"), ("Wszystkie pliki", ".*")))
        
        # add file path to the listbox        
        for file in self.filepaths:
            self.list_box.insert(tk.END, file)

    def execute(self):
        if hasattr (self, 'filepaths'):
            for file in self.filepaths:

                # method for open file 
                X_cord, Y_cord, Z_cord = self.open_file(file)
                X_cord = np.array(X_cord, dtype=float)
                Y_cord = np.array(Y_cord, dtype=float)
                Z_cord = np.array(Z_cord, dtype=float)

                # radius and center
                center, radius = self.circle_mean(X_cord=X_cord, Y_cord=Y_cord)

                # Create a new set of axes for each file
                # ax = self.fig.add_subplot(111)
                circle = Circle(center, radius, fill=False)
                print(f"circle: {circle}")
                # self.ax.add_patch(circle)

                self.ax.autoscale()

                self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.master)
                self.canvas.draw()
                self.canvas.get_tk_widget().place(x=30, y=200)

                # calculate step 
                circuit = 2*np.pi*radius
                step = circuit/len(X_cord)

                # instance of class signal_to_tf
                signal_ = signal_to_tf(step=step, Z_cord=Z_cord)

                # method of signal_to_tf
                positive_ampli, positive_freq, positive_phase  = signal_.DFT_method()
                steps = signal_.steps
                signals, sum_signals = signal_.dominant_components(ampli=positive_ampli, freq=positive_freq, phase=positive_phase)

                self.ax.plot(steps, Z_cord)
                self.ax_domein.plot(steps, sum_signals)
                self.ax_dft.plot(positive_freq, positive_ampli)
                self.ax_dft.set_xlim(0, 0.1)

            return step, Z_cord

if __name__ == "__main__":
    root = tk.Tk()
    app = AppToTest(root)
    root.mainloop()
