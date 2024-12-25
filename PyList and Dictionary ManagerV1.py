import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import json

class ListDictManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("List and Dictionary Manager")
        self.geometry("1200x800")

        # Data structures
        self.my_list = []
        self.my_dict = {}

        # Quoting option
        self.quote_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Wrap strings in quotes", variable=self.quote_var).grid(row=6, column=0, columnspan=2)

        # List Controls
        tk.Label(self, text="List Operations").grid(row=0, column=0, columnspan=2)
        self.list_entry = tk.Entry(self, bd=12, bg="light sky blue", width=20)
        self.list_entry.grid(row=1, column=0)
        tk.Button(self, bd=7, bg="thistle", text="Add to List", command=self.add_to_list).grid(row=1, column=1)
        tk.Button(self, bd=7, bg="HotPink1", text="Remove from List", command=self.remove_from_list).grid(row=2, column=1)
        tk.Button(self, bd=7, bg="LightSalmon2", text="Save List", command=self.save_list).grid(row=3, column=0)
        tk.Button(self, bd=7, bg="MistyRose2", text="Save List as Text", command=self.save_list_as_txt).grid(row=3, column=2)
        tk.Button(self, bd=7, bg="PeachPuff2", text="Load List", command=self.load_list).grid(row=3, column=3)
        tk.Button(self, bd=7, bg="NavajoWhite2", text="Load List as Text", command=self.load_list_as_txt).grid(row=3, column=4)
        tk.Button(self, bd=7, bg="SeaGreen1", text="CSV to List", command=self.csv_to_list).grid(row=4, column=0, columnspan=2)
        self.listbox = tk.Listbox(self, bd=12, bg="light cyan", width=30)
        self.listbox.grid(row=5, column=0, columnspan=2)

        # Dictionary Controls
        tk.Label(self, text="Dictionary Operations").grid(row=0, column=2, columnspan=3)
        tk.Label(self, text="Key:").grid(row=1, column=2)
        self.dict_key_entry = tk.Entry(self, bd=11, bg="wheat", width=10)
        self.dict_key_entry.grid(row=1, column=3)
        tk.Label(self, text="Value:").grid(row=1, column=4)
        self.dict_value_entry = tk.Entry(self, bd=11, bg="thistle", width=10)
        self.dict_value_entry.grid(row=1, column=5)
        tk.Button(self, bd=7, bg="aquamarine", text="Add to Dict", command=self.add_to_dict).grid(row=2, column=5)
        tk.Button(self, bd=7, bg="khaki", text="Remove from Dict", command=self.remove_from_dict).grid(row=4, column=5)
        tk.Button(self, bd=7, bg="sky blue", text="Save Dict", command=self.save_dict).grid(row=3, column=5)
        tk.Button(self, bd=7, bg="plum1", text="Load Dict", command=self.load_dict).grid(row=3, column=6)
        tk.Button(self, bd=7, bg="gold", text="JSON to Dict", command=self.json_to_dict).grid(row=12, column=2, columnspan=2)
        tk.Button(self, text="Help", command=self.show_help, bd=7, bg="light goldenrod").grid(row=12, column=0, columnspan=2)
        tk.Button(self, text=" Program Overview", command=self.overview, bd=7, bg="cyan").grid(row=13, column=2, columnspan=2)
        self.treeview = ttk.Treeview(self, columns=("Key", "Value"), show="headings")
        self.treeview.grid(row=7, column=2, columnspan=3)
        self.treeview.heading("Key", text="Key")
        self.treeview.heading("Value", text="Value")

    def add_to_list(self):
        item = self.list_entry.get()
        if item:
            self.my_list.append(item)
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Please enter a value to add.")

    def remove_from_list(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            self.my_list.pop(index)
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Please select an item to remove.")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.my_list:
            self.listbox.insert(tk.END, item)

    def save_list_as_txt(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                for item in self.my_list:
                    file.write(f"{item}\n")
            messagebox.showinfo("Success", "List saved successfully.")

    def save_list(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write("my_list = [\n")
                for item in self.my_list:
                    if self.quote_var.get():
                        file.write(f"    {repr(item)},\n")
                    else:
                        file.write(f"    {item},\n")
                file.write("]\n")
            messagebox.showinfo("Success", "List saved as Python file successfully.")

    def load_list(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            try:
                if file_path.endswith(".py"):
                    with open(file_path, "r") as file:
                        local_vars = {}
                        exec(file.read(), {}, local_vars)
                        self.my_list = local_vars.get("my_list", [])
                else:
                    with open(file_path, "r") as file:
                        self.my_list = [line.strip().strip("'\"") if self.quote_var.get() else line.strip() for line in file]
                self.update_listbox()
                messagebox.showinfo("Success", "List loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load list: {e}")

    def load_list_as_txt(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.my_list = [line.strip() for line in file]
            self.update_listbox()
            messagebox.showinfo("Success", "List loaded successfully.")

    def csv_to_list(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                self.my_list = [row for row in reader]
            self.update_listbox()
            messagebox.showinfo("Success", "CSV converted to list.")

    def add_to_dict(self):
        key = self.dict_key_entry.get()
        value = self.dict_value_entry.get()
        if key and value:
            self.my_dict[key] = value
            self.update_treeview()
        else:
            messagebox.showwarning("Warning", "Please enter both key and value.")

    def remove_from_dict(self):
        selected = self.treeview.selection()
        if selected:
            for item in selected:
                key = self.treeview.item(item, "values")[0]
                self.my_dict.pop(key, None)
            self.update_treeview()
        else:
            messagebox.showwarning("Warning", "Please select an item to remove.")

    def update_treeview(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        for key, value in self.my_dict.items():
            self.treeview.insert("", tk.END, values=(key, value))

    def save_dict(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                if self.quote_var.get():
                    json.dump({repr(k): repr(v) for k, v in self.my_dict.items()}, file)
                else:
                    json.dump(self.my_dict, file)
            messagebox.showinfo("Success", "Dictionary saved successfully.")

    def load_dict(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    data = json.load(file)
                    if self.quote_var.get():
                        self.my_dict = {k.strip("'\""): v.strip("'\"") for k, v in data.items()}
                    else:
                        self.my_dict = data
                self.update_treeview()
                messagebox.showinfo("Success", "Dictionary loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dictionary: {e}")

    def json_to_dict(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.my_dict = json.load(file)
            self.update_treeview()
            messagebox.showinfo("Success", "JSON converted to dictionary.")

    def overview(self):
        overview_str = """    Program Overview
        The List and Dictionary Manager is a versatile GUI application built using Python's tkinter module. It provides tools for managing and manipulating lists and dictionaries through an intuitive interface. Key features include:

        List Management:

        Add and remove items from a list.
        Save lists as Python files or text files.
        Load lists from Python or text files.
        Convert CSV files to lists.
        Dictionary Management:

        Add and remove key-value pairs in a dictionary.
        Save dictionaries as JSON files.
        Load dictionaries from JSON files.
        Convert JSON files to dictionaries.
        Interactive Widgets:

        A Listbox for displaying and managing list items.
        A Treeview for displaying dictionary key-value pairs.
        File Handling:

        Easily load and save data to/from files.
        Supports .txt, .py, .csv, and .json file formats."""
        messagebox.showinfo("Overview of the programs", overview_str)

    def show_help(self):
        help_text = (
            "Welcome to the List and Dictionary Manager!\n\n"
            "This program allows you to manage lists and dictionaries interactively. Here’s how to use it:\n\n"
            "List Operations:\n"
            "- Enter an item in the text box and click 'Add to List' to add it.\n"
            "- Select an item from the listbox and click 'Remove from List' to delete it.\n"
            "- Save your list as a text or Python file using 'Save List' or 'Save List as Text'.\n"
            "- Load an existing list from a text or Python file using 'Load List' or 'Load List as Text'.\n"
            "- Convert a CSV file into a list using 'CSV to List'.\n\n"
            "Dictionary Operations:\n"
            "- Enter a key and value in the respective fields and click 'Add to Dict' to add it.\n"
            "- Select an entry from the dictionary table and click 'Remove from Dict' to delete it.\n"
            "- Save your dictionary as a JSON file using 'Save Dict'.\n"
            "- Load an existing dictionary from a JSON file using 'Load Dict'.\n"
            "- Convert a JSON file into a dictionary using 'JSON to Dict'.\n\n"
            "Tips:\n"
            "- Use the file dialogs to easily browse and select files for saving and loading.\n"
            "- Data structures will be displayed in the listbox (for lists) and the treeview (for dictionaries).\n\n"
            "Enjoy managing your data efficiently!"
        )
        messagebox.showinfo("Help - List and Dictionary Manager", help_text)

if __name__ == "__main__":
    app = ListDictManager()
    app.mainloop()
