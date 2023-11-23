import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import json
import os

class CustomCommandsManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Custom Commands")

        # Load existing command-program associations from commands.json
        self.command_program_dict = self.load_command_program_dict()

        # Create a listbox to display custom commands
        self.custom_commands_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=10, width=50, font=("Arial", 12))
        self.custom_commands_listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Populate the listbox with existing custom commands
        self.update_custom_commands_listbox()

        # Buttons for adding, deleting, and closing
        add_custom_button = tk.Button(self.root, text="Add Custom Command", command=self.add_custom_command)
        add_custom_button.pack(pady=5, ipadx=10)

        delete_custom_button = tk.Button(self.root, text="Delete Custom Command", command=self.delete_custom_command)
        delete_custom_button.pack(pady=5, ipadx=10)

        close_button = tk.Button(self.root, text="Close", command=self.root.destroy)
        close_button.pack(pady=5, ipadx=10)

    def load_command_program_dict(self):
        # Load command-program associations from commands.json
        file_path = os.path.join(os.getcwd(), "commands.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as commands_file:
                return json.load(commands_file)
        else:
            return {}

    def update_custom_commands_listbox(self):
        # Clear the listbox and repopulate with custom commands
        self.custom_commands_listbox.delete(0, tk.END)
        for command, program in self.command_program_dict.items():
            self.custom_commands_listbox.insert(tk.END, f"{command} - {program}")

    def add_custom_command(self):
        # Ask the user for the custom command
        custom_command = simpledialog.askstring("Add Custom Command", "Enter the custom command:")
        if custom_command:
            # Ask the user for the program associated with the command
            program_path = filedialog.askopenfilename(title=f"Select a program for '{custom_command}' command")
            if program_path:
                # Save the command-program association to the dictionary
                self.command_program_dict[custom_command] = program_path

                # Save the command-program dictionary to a file
                self.save_command_program_dict()

                self.update_custom_commands_listbox()

    def delete_custom_command(self):
        # Get the selected custom command
        selected_index = self.custom_commands_listbox.curselection()
        if selected_index:
            selected_command = self.custom_commands_listbox.get(selected_index)
            selected_command = selected_command.split(" - ")[0]  # Extract command from the listbox entry

            # Confirm with the user before deleting
            confirmation = messagebox.askyesno(
                "Confirmation",
                f"Do you really want to delete the custom command '{selected_command}'?"
            )

            if confirmation:
                # Remove the selected custom command from the dictionary
                del self.command_program_dict[selected_command]

                # Save the updated command-program dictionary to a file
                self.save_command_program_dict()

                self.update_custom_commands_listbox()

    def save_command_program_dict(self):
        # Save the command-program dictionary to a file (e.g., commands.json)
        file_path = os.path.join(os.getcwd(), "commands.json")
        with open(file_path, "w") as commands_file:
            json.dump(self.command_program_dict, commands_file)

    def get_command_program_dict(self):
        # Return the command_program_dict
        return self.command_program_dict

if __name__ == "__main__":
    manager = CustomCommandsManager()
    manager.root.mainloop()
