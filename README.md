This Python code implements a GUI application for simulating the Shortest Job First (SJF) CPU scheduling algorithm. Let's break down how it works:

1. **Importing Libraries**:
   - `tkinter`: For creating the GUI.
   - `ttk`: For creating themed widgets in tkinter.
   - `messagebox`: For displaying error messages.
   - `deque`: For implementing a queue with efficient insertion and deletion from both ends.

2. **Process Class**:
   - Represents a process with attributes such as process ID (`pid`), arrival time, burst time, remaining time, start time, end time, waiting time, turnaround time, and response time.

3. **SJF_GUI Class**:
   - Manages the GUI and scheduling logic.
   - Initializes the tkinter GUI with labels, entry fields, buttons, canvas for Gantt chart, and text box for displaying results.
   - `create_widgets`: Sets up the initial widgets in the GUI.
   - `get_processes`: Gets the number of processes from the user and creates entry fields for entering process details.
   - `create_process_entries`: Creates entry fields for each process to input arrival time and burst time.
   - `schedule_processes`: Handles the submission of process details, creates `Process` objects, and starts the SJF scheduling algorithm.
   - `run_sjf`: Implements the SJF scheduling algorithm.
     - Processes are sorted based on arrival time.
     - While there are processes or processes in the ready queue:
       - Processes arriving at the current time are added to the ready queue.
       - The process with the shortest remaining time in the ready queue is selected.
       - The selected process executes for one time unit.
       - If a process completes execution, its end time and turnaround time are calculated, and it's removed from the ready queue.
       - Otherwise, it's added back to the ready queue.
   - `calculate_results`: Calculates and stores average waiting time, turnaround time, and response time for the completed processes.
   - `display_results`: Displays the Gantt chart and results in the GUI.
   
4. **Main Function**:
   - Creates a tkinter root window and initializes an instance of `SJF_GUI`.
   - Starts the GUI main loop.

Overall, the program provides a user-friendly interface to input process details, simulates the SJF scheduling algorithm, and displays the Gantt chart and scheduling results.
