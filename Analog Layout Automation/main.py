import tkinter as tk
from tkinter import simpledialog
import init_dir
import open_cell_view
import needed_functions
import subprocess
import DRC_check
import LVS_check
# initialize Cadence directory if not already initialized
if not needed_functions.check_file_exists("cds.lib"):
    init_dir.cdslib()
if not needed_functions.check_file_exists(".cdsinit"):
    init_dir.cdsinit()
if not needed_functions.check_file_exists(".cdsenv"):
    init_dir.cdsenv()

# Create root window
root = tk.Tk()
root.geometry("800x500+500+200")
root.title("Analog Layout Automation tool")

# Define colors for a more visually appealing design
background_color = "#2b2b2b"  # dark gray
button_color = "#4f5b66"  # lighter gray
text_color = "#d8dee9"  # light blue-gray

# Apply background color to root window
root.configure(bg=background_color)


def create_new_cell_view():
    library_name = simpledialog.askstring("Input", "library name:")
    cell_view_name = simpledialog.askstring("Input", "cell view name:")
    open_cell_view.create_il_file(library_name, cell_view_name)
    open_cell_view.run_virtuoso(cell_view_name)


def open_existing_cell_view():
    existing_cell_views = needed_functions.library_cell_view_dict()

    def open_value_window(key, dict_data):
        value_win = tk.Toplevel()
        value_win.title("Cell view")
        lst = tk.Listbox(value_win)
        lst.insert(tk.END, *dict_data[key])
        lst.pack(pady=10)

        def on_value_select(evt):
            w = evt.widget
            if w.curselection():
                index = int(w.curselection()[0])
                value = w.get(index)
                value_win.destroy()
                needed_functions.extract(key, value)
                subprocess.call(["python3", "run.py"])
                needed_functions.edit_run_skill_il(key, value)
                subprocess.call(["virtuoso", "-nograph", "-restore", "run_skill.il"])

        lst.bind('<<ListboxSelect>>', on_value_select)

    def on_key_select(evt):
        w = evt.widget
        if w.curselection():
            index = int(w.curselection()[0])
            key = w.get(index)
            key_win.destroy()
            open_value_window(key, existing_cell_views)

    key_win = tk.Toplevel()
    key_win.title("Library")
    lst = tk.Listbox(key_win)
    lst.insert(tk.END, *existing_cell_views.keys())
    lst.pack(pady=10)
    lst.bind('<<ListboxSelect>>', on_key_select)


# Create buttons with custom color and text color
cell_view_button = tk.Button(root, text="create Cell view", command=create_new_cell_view,
                             bg=button_color, fg=text_color, font='Helvetica 12 bold')
cell_view_button.pack(side=tk.LEFT, padx=100)

existing_cell_view_button = tk.Button(root, text="Open existing cell view", command=open_existing_cell_view,
                           bg=button_color, fg=text_color, font='Helvetica 12 bold')
existing_cell_view_button.pack(side=tk.RIGHT, padx=100)

root.mainloop()
