import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import os
import base64

# File name for saving notes
NOTES_FILE = "notes_data.json"


class NoteTaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Taker")
        # Initialize the GUI components
        self.init_gui()

        # Load existing notes
        self.update_notes_listbox()

    def init_gui(self):
        # Styles for ttk widgets
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#55acee")
        style.map("TButton",
                  foreground=[('pressed', 'white'), ('active', 'black')],
                  background=[('pressed', '!disabled', 'black'), ('active', '#55acee')])

        # Textbox to enter note
        self.note_entry = tk.Text(self.root, width=40, height=5, font=("Arial", 12))
        self.note_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Buttons
        add_button = ttk.Button(self.root, text="Add Note", command=self.add_note)
        add_button.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        attach_button = ttk.Button(self.root, text="Attach File", command=self.attach_file)
        attach_button.grid(row=0, column=4, padx=5, pady=10, sticky="ew")

        view_button = ttk.Button(self.root, text="View Notes", command=self.view_notes)
        view_button.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

        delete_button = ttk.Button(self.root, text="Delete Note", command=self.delete_note)
        delete_button.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

        # Additional variables to store attached file paths and names
        self.attached_files = {}

        # Listbox to display notes
        self.notes_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=10, width=50, font=("Arial", 12))
        self.notes_listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Scrollbar for the listbox
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.notes_listbox.yview)
        scrollbar.grid(row=1, column=4, sticky="ns")
        self.notes_listbox.config(yscrollcommand=scrollbar.set)

        # Configure row and column weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # Bind enter key to the Add Note button
        self.root.bind('<Return>', lambda event=None: add_button.invoke())

    def attach_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "rb") as file:
                file_data = base64.b64encode(file.read()).decode('utf-8')
                self.attached_files[len(self.attached_files)] = {"data": file_data, "name": os.path.basename(file_path)}
                messagebox.showinfo("File Attached", f"File attached successfully: {file_path}")
                self.note_entry.insert(tk.END, f"\nAttached File: {os.path.basename(file_path)}")

    def add_note(self):
        note_text = self.note_entry.get("1.0", tk.END).strip()
        if note_text:
            notes_data = self.load_notes()
            notes_data["notes"].append({"text": note_text, "attachments": self.attached_files})

            self.save_notes(notes_data)

            messagebox.showinfo("Note Added", "Note added successfully.")
            self.note_entry.delete("1.0", tk.END)  # Clear the entry field
            self.update_notes_listbox()
        else:
            messagebox.showwarning("Empty Note", "Please enter a note before adding.")

    def view_notes(self):
        notes_data = self.load_notes()
        notes_list = notes_data["notes"]

        if not notes_list:
            messagebox.showinfo("No Notes", "No notes available.")
            return

        notes_text = ""
        for idx, note in enumerate(notes_list, start=1):
            notes_text += f"{idx}. {note['text']}\n"

            # Display attached files
            attached_files = note.get('attachments', {})
            for file_index, file_data in attached_files.items():
                notes_text += f"    Attached File {file_index}: {file_data['name']}\n"

        if notes_text:
            messagebox.showinfo("Your Notes", notes_text)
            self.open_attached_files(notes_list)
        else:
            messagebox.showinfo("No Notes", "No notes or attached files available.")

    def open_attached_files(self, notes_list):
        for note in notes_list:
            attached_files = note.get('attachments', {})
            for file_index, file_data in attached_files.items():
                # Use the original file extension for the temporary file
                temp_file_extension = os.path.splitext(file_data['name'])[1]
                temp_file_path = f"temp_file_{file_index}{temp_file_extension}"
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(base64.b64decode(file_data['data']))

                # Open the file using the default application
                os.system(f'start {temp_file_path}')


    def delete_note(self):
        notes_data = self.load_notes()
        notes_list = notes_data["notes"]

        if not notes_list:
            messagebox.showinfo("No Notes", "No notes available.")
            return

        try:
            note_index = int(simpledialog.askstring("Delete Note", "Enter the index of the note you want to delete:"))
            if 1 <= note_index <= len(notes_list):
                deleted_note = notes_list.pop(note_index - 1)
                self.save_notes(notes_data)
                messagebox.showinfo("Note Deleted", f"Note {note_index} deleted: {deleted_note['text']}")
                self.update_notes_listbox()
            else:
                messagebox.showwarning("Invalid Index", "Invalid note index.")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid note index.")

    def update_notes_listbox(self):
        self.notes_listbox.delete(0, tk.END)  # Clear the listbox
        notes_data = self.load_notes()
        notes_list = notes_data["notes"]
        for note in notes_list:
            self.notes_listbox.insert(tk.END, note['text'])

    def load_notes(self):
        try:
            with open(NOTES_FILE, "r") as file:
                notes_data = json.load(file)

                # Handle the case where "attached_files" might be a list
                if isinstance(notes_data.get("attached_files"), list):
                    notes_data["attached_files"] = {}

                # Decode attached files from Base64 after loading
                notes_data["attached_files"] = {
                    key: {"data": base64.b64decode(value['data'].encode('utf-8')), "name": value['name']}
                    for key, value in notes_data.get("attached_files", {}).items()
                }

                return notes_data
        except FileNotFoundError:
            return {"notes": []}
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding JSON file.")
            return {"notes": []}

    def save_notes(self, notes_data):
        try:
            # Encode attached files to Base64 before saving
            notes_data["attached_files"] = {
                key: {"data": base64.b64encode(value['data']).decode('utf-8'), "name": value['name']}
                for key, value in notes_data.get("attached_files", {}).items()
            }

            with open(NOTES_FILE, "w") as file:
                json.dump(notes_data, file, default=self.json_default)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error encoding JSON data.")

    def json_default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        raise TypeError


def create_note_taker():
    root = tk.Tk()
    note_taker = NoteTaker(root)
    return note_taker


if __name__ == "__main__":
    create_note_taker().root.mainloop()
