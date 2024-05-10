import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.end_time = None
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = None

class SJF_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shortest Job First (SJF) Scheduler")

        self.processes = []
        self.current_process = None
        self.current_time = 0
        self.ready_queue = deque()
        self.completed_processes = []

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")  # Use the "clam" theme for a modern look

        self.processes_frame = ttk.Frame(self.root)
        self.processes_frame.pack(padx=20, pady=10)

        self.process_label = ttk.Label(self.processes_frame, text="Enter number of processes:")
        self.process_label.grid(row=0, column=0, padx=5, pady=5)
        self.process_entry = ttk.Entry(self.processes_frame)
        self.process_entry.grid(row=0, column=1, padx=5, pady=5)
        self.submit_button = ttk.Button(self.processes_frame, text="Submit", command=self.get_processes)
        self.submit_button.grid(row=0, column=2, padx=5, pady=5)

        self.gantt_chart_label = ttk.Label(self.root, text="Gantt Chart")
        self.gantt_chart_label.pack(pady=10)

        self.gantt_chart_canvas = tk.Canvas(self.root, width=600, height=100)
        self.gantt_chart_canvas.pack()

        self.results_label = ttk.Label(self.root, text="Results")
        self.results_label.pack(pady=10)

        self.results_text = tk.Text(self.root, width=50, height=10)
        self.results_text.pack()

    def get_processes(self):
        try:
            num_processes = int(self.process_entry.get())
            if num_processes <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of processes.")
            return

        self.processes_frame.destroy()
        self.create_process_entries(num_processes)

    def create_process_entries(self, num_processes):
        self.process_entries = []
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.schedule_processes)
        self.submit_button.pack(pady=10)

        for i in range(num_processes):
            frame = ttk.Frame(self.root)
            frame.pack(padx=20, pady=5)
            process_label = ttk.Label(frame, text=f"Process {i+1}:")
            process_label.grid(row=0, column=0, padx=5, pady=5)
            arrival_label = ttk.Label(frame, text="Arrival Time:")
            arrival_label.grid(row=0, column=1, padx=5, pady=5)
            burst_label = ttk.Label(frame, text="Burst Time:")
            burst_label.grid(row=0, column=3, padx=5, pady=5)

            pid_entry = ttk.Entry(frame)
            pid_entry.grid(row=i+1, column=0, padx=5, pady=5)
            arrival_entry = ttk.Entry(frame)
            arrival_entry.grid(row=i+1, column=1, padx=5, pady=5)
            burst_entry = ttk.Entry(frame)
            burst_entry.grid(row=i+1, column=3, padx=5, pady=5)

            self.process_entries.append((pid_entry, arrival_entry, burst_entry))

    def schedule_processes(self):
        self.submit_button.destroy()
        for entry_set in self.process_entries:
            try:
                pid = int(entry_set[0].get())
                arrival_time = int(entry_set[1].get())
                burst_time = int(entry_set[2].get())
                if pid <= 0 or arrival_time < 0 or burst_time <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter valid process information.")
                return
            self.processes.append(Process(pid, arrival_time, burst_time))

        self.run_sjf()

    def run_sjf(self):
        self.processes.sort(key=lambda x: x.arrival_time)

        while self.processes or self.ready_queue:
            while self.processes and self.processes[0].arrival_time <= self.current_time:
                self.ready_queue.append(self.processes.pop(0))

            if self.ready_queue:
                self.ready_queue = deque(sorted(self.ready_queue, key=lambda x: x.remaining_time))
                current_process = self.ready_queue.popleft()

                if current_process.start_time is None:
                    current_process.start_time = self.current_time
                    current_process.response_time = self.current_time - current_process.arrival_time

                current_process.remaining_time -= 1
                self.current_time += 1

                if current_process.remaining_time == 0:
                    current_process.end_time = self.current_time
                    current_process.turnaround_time = current_process.end_time - current_process.arrival_time
                    self.completed_processes.append(current_process)
                else:
                    self.ready_queue.append(current_process)

            else:
                self.current_time += 1

        self.calculate_results()
        self.display_results()

    def calculate_results(self):
        total_waiting_time = 0
        total_turnaround_time = 0
        total_response_time = 0

        for process in self.completed_processes:
            process.waiting_time = process.start_time - process.arrival_time
            total_waiting_time += process.waiting_time
            total_turnaround_time += process.turnaround_time
            total_response_time += process.response_time

        self.avg_waiting_time = total_waiting_time / len(self.completed_processes)
        self.avg_turnaround_time = total_turnaround_time / len(self.completed_processes)
        self.avg_response_time = total_response_time / len(self.completed_processes)

    def display_results(self):
        gantt_width = 600
        gantt_height = 100
        cell_width = gantt_width / self.current_time

        for i, process in enumerate(self.completed_processes):
            start = process.start_time * cell_width
            end = process.end_time * cell_width
            self.gantt_chart_canvas.create_rectangle(start, i*20, end, (i+1)*20, fill="sky blue")
            self.results_text.insert(tk.END, f"Process {process.pid}:\n")
            self.results_text.insert(tk.END, f"\tWaiting Time: {process.waiting_time}\n")
            self.results_text.insert(tk.END, f"\tTurnaround Time: {process.turnaround_time}\n")
            self.results_text.insert(tk.END, f"\tResponse Time: {process.response_time}\n\n")

        self.results_text.insert(tk.END, f"Average Waiting Time: {self.avg_waiting_time}\n")
        self.results_text.insert(tk.END, f"Average Turnaround Time: {self.avg_turnaround_time}\n")
        self.results_text.insert(tk.END, f"Average Response Time: {self.avg_response_time}\n")

if __name__ == "__main__":
    root = tk.Tk()
    sjf_gui = SJF_GUI(root)
    root.mainloop()

