# Here is the code I used, which you can try running on your local machine:

import tkinter as tk
from tkinter import filedialog
import pandas as pd

from LogProcessor import LogProcessor


def open_file():
    global file_path
    global lp1

    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.txt")])
    lp1 = LogProcessor(file_path)
    print(file_path)
    if file_path:
        df = pd.read_csv(file_path)
        print(df.head())  # Display the first few rows of the dataframe

def get_error_msg_only():
    print(file_path)
    lp1.get_error_logs()

def get_error_summary():
    lp1.get_error_summary()


def get_error_plots():
    lp1.get_error_plot()


# Create the main window
root = tk.Tk()
root.title("Error Msg Extractor")

# Create a button to open the file dialog
upload_button = tk.Button(root, text="Upload CSV File", command=open_file)
upload_button.pack(pady=50)

#Create a button that processes the file by error types and gives error
error_button = tk.Button(root, text="Get Error Logs", command=get_error_msg_only)
error_button.pack(pady=50,padx =50)

error_summary_button = tk.Button(root, text="Get Error Summary", command=get_error_summary)
error_summary_button.pack(pady=50,padx =50)

error_graph_button = tk.Button(root, text="Get Error Plots", command=get_error_plots)
error_graph_button.pack(pady=50,padx =50)



# Run the application
root.mainloop()