import tkinter as tk
from tkinter import simpledialog, PhotoImage
from PIL import Image, ImageTk
import json

# File name for saving data
data_file = "expenses_data.json"

# Function to load saved data (if any)
def load_data():
    try:
        with open(data_file, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {"expenses": {}, "category_totals": {}}

# Initialize data dictionaries
data = load_data()
expenses = data["expenses"]
category_totals = data["category_totals"]
categories = ["Education", "Food", "Transport", "Misc"]

# Function to save data
def save_data():
    with open(data_file, "w") as file:
        json.dump(data, file)

# Function to create the expense manager window
def create_expense_manager():
    def add_expense():
        name = name_entry.get()
        amount = amount_entry.get()
        category = category_var.get()

        if name and amount:
            amount = float(amount)
            # Add the expense to the expenses dictionary
            if category not in expenses:
                expenses[category] = []
            expenses[category].append((name, amount))

            # Update the category totals
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += amount

            update_tables()
            save_data()

            name_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)

    def on_closing():
        save_data()
        expense_root.destroy()

    def update_tables():
        update_expenses_list()
        update_category_totals()

    def update_expenses_list():
        expenses_label.config(text="All Expenses")

        # Clear the previous entries
        for widget in expenses_frame.winfo_children():
            widget.grid_forget()

        row = 1
        for category in categories:
            if category in expenses:
                tk.Label(expenses_frame, text=f"{category} Expenses:", font=("Arial", 16, "bold")).grid(row=row, column=0, columnspan=2)
                row += 1
                for name, amount in expenses[category]:
                    tk.Label(expenses_frame, text=name, font=("Arial", 12)).grid(row=row, column=0)
                    tk.Label(expenses_frame, text=f"₹{amount:.2f}", font=("Arial", 12)).grid(row=row, column=1)
                    row += 1

    def update_category_totals():
        for widget in totals_frame.winfo_children():
            widget.grid_forget()

        tk.Label(totals_frame, text="Category Totals", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2)

        row = 1
        for category in categories:
            total = category_totals.get(category, 0)
            tk.Label(totals_frame, text=f"{category} Total:", font=("Arial", 12)).grid(row=row, column=0)
            tk.Label(totals_frame, text=f"₹{total:.2f}", font=("Arial", 12)).grid(row=row, column=1)
            row += 1

        complete_total = sum(category_totals.values())
        tk.Label(totals_frame, text="Complete Total:", font=("Arial", 14, "bold")).grid(row=row, column=0)
        tk.Label(totals_frame, text=f"₹{complete_total:.2f}", font=("Arial", 14, "bold")).grid(row=row, column=1)

    def delete_expense():
        category = category_var.get()
        if category in expenses and expenses[category]:
            # Assuming you want to delete the most recently added expense
            removed_expense = expenses[category].pop()
            
            # Update the category totals
            category_totals[category] -= removed_expense[1]

            # Update the complete total
            complete_total = sum(category_totals.values())

            # Save the data
            save_data()

            # Update the tables
            update_tables()

    expense_root = tk.Toplevel()
    expense_root.title("Expense Manager")

    input_frame = tk.Frame(expense_root)
    input_frame.grid(row=0, column=0)

    expenses_frame = tk.Frame(expense_root)
    expenses_frame.grid(row=1, column=0)

    totals_frame = tk.Frame(expense_root)
    totals_frame.grid(row=0, column=1, rowspan=2)

    name_label = tk.Label(input_frame, text="Expense Name:", font=("Arial", 16))
    name_label.grid(row=0, column=0)
    name_entry = tk.Entry(input_frame, font=("Arial", 14))
    name_entry.grid(row=0, column=1)

    amount_label = tk.Label(input_frame, text="Expense Amount:", font=("Arial", 16))
    amount_label.grid(row=1, column=0)
    amount_entry = tk.Entry(input_frame, font=("Arial", 14))
    amount_entry.grid(row=1, column=1)

    category_label = tk.Label(input_frame, text="Expense Category:", font=("Arial", 16))
    category_label.grid(row=2, column=0)

    category_var = tk.StringVar(input_frame)
    category_var.set(categories[0])
    category_option = tk.OptionMenu(input_frame, category_var, *categories)
    category_option.grid(row=2, column=1)

    add_button = tk.Button(input_frame, text="Add Expense", command=add_expense, font=("Arial", 16, "bold"))
    add_button.grid(row=3, column=0, columnspan=2)

    update_button = tk.Button(input_frame, text="Update Tables", command=update_tables, font=("Arial", 16, "bold"))
    update_button.grid(row=4, column=0, columnspan=2)

    # Create a button to delete an expense
    delete_button = tk.Button(input_frame, text="Delete Expense", command=delete_expense, font=("Arial", 16, "bold"))
    delete_button.grid(row=5, column=0, columnspan=2)

    expenses_label = tk.Label(expenses_frame, text="All Expenses", font=("Arial", 16, "bold"))
    totals_label = tk.Label(totals_frame, text="Category Totals", font=("Arial", 16, "bold"))

    update_tables()

    expense_root.protocol("WM_DELETE_WINDOW", on_closing)
    expense_root.mainloop()

if __name__ == "__main__":
    create_expense_manager()
