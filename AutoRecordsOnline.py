##############################################################################
# Name: Oliver Tipping
# Date: 07/16/23
# Program: Auto Records Online
#############################################################################
import tkinter as tk
from tkinter import ttk, messagebox
import time

import fcntl  # For file locking

def validate_login(username, password):
    # You can implement your own login validation logic here
    with open("application.txt", "w") as applicationfile:
        applicationfile.write("Authenticate Login " + username + " " + password)

    # Wait for a moment to allow the file to be written by other processes
    time.sleep(1)

    # Open the file in "r" mode and apply an exclusive lock
    with open("application.txt", "r") as applicationfile:
        fcntl.flock(applicationfile, fcntl.LOCK_EX)  # Lock the file for exclusive access
        applicationfile.seek(0)  # Reset the file pointer to the beginning
        loginCommand = applicationfile.read().split()
        fcntl.flock(applicationfile, fcntl.LOCK_UN)  # Release the lock

    if len(loginCommand) == 3 and loginCommand[1] == "Complete":
        return True
    else:
        return False
    
def create_account(username, password):
    # You can implement your own logic here to handle the account creation
    with open("application.txt", "w") as applicationfile:
        applicationfile.write("Authenticate New " + username + " " + password + " user")

    # Wait for a moment to allow the file to be written by other processes
    time.sleep(1)

    # Open the file in "r" mode and apply an exclusive lock
    with open("application.txt", "r") as applicationfile:
        fcntl.flock(applicationfile, fcntl.LOCK_EX)  # Lock the file for exclusive access
        applicationfile.seek(0)  # Reset the file pointer to the beginning
        loginCommand = applicationfile.read().split()
        fcntl.flock(applicationfile, fcntl.LOCK_UN)  # Release the lock

    if loginCommand[1] == "Complete":
        messagebox.showinfo("Account Creation", "Account created successfully.")
    else:
        messagebox.showinfo("Account Creation", "Account Creation Failed.")

def login():
    username = username_entry.get()
    password = password_entry.get()

    if validate_login(username, password):
        login_window.destroy()  # Close the login window
        show_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def show_main_window():
    main_window = tk.Tk()
    main_window.title("Auto Records Online")

    def select_item(event):
        selected_item = treeview.focus()
        if selected_item:
            pass

    def add_item():
        vehicle_id = vehicle_entry.get()
        if vehicle_id:
            treeview.insert('', 'end', values=(vehicle_id,))
            vehicle_window.destroy()

    def open_vehicle_window():
        global vehicle_window
        vehicle_window = tk.Toplevel(main_window)
        vehicle_window.title("Add Vehicle")
        vehicle_window.geometry("300x100")

        vehicle_label = ttk.Label(vehicle_window, text="Vehicle ID:")
        vehicle_label.pack()

        global vehicle_entry
        vehicle_entry = ttk.Entry(vehicle_window)
        vehicle_entry.pack()

        add_button = ttk.Button(vehicle_window, text="Add", command=add_item)
        add_button.pack(pady=10)

    def delete_item():
        selected_item = treeview.focus()
        if selected_item:
            item_values = treeview.item(selected_item)['values']
            if item_values:
                confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected vehicle?")
                if confirm:
                    treeview.delete(selected_item)

    def open_view_window():
        view_window = tk.Toplevel(main_window)
        view_window.title("View Records")
        view_window.geometry("400x300")

        # Create a scrollable treeview
        treeview = ttk.Treeview(view_window, columns=("Date", "Description"), show="headings")
        treeview.column("Date", width=150)
        treeview.heading("Date", text="Date")
        treeview.column("Description", width=200)
        treeview.heading("Description", text="Description")
        treeview.pack(fill=tk.BOTH, expand=True)

        # Create entry fields frame
        entry_frame = ttk.Frame(view_window)
        entry_frame.pack(pady=10)

        # Date label and entry
        date_label = ttk.Label(entry_frame, text="Date:")
        date_label.grid(row=0, column=0, sticky=tk.W)
        date_entry = ttk.Entry(entry_frame)
        date_entry.grid(row=0, column=1, padx=5)

        # Description label and entry
        description_label = ttk.Label(entry_frame, text="Description:")
        description_label.grid(row=1, column=0, sticky=tk.W)
        description_entry = ttk.Entry(entry_frame)
        description_entry.grid(row=1, column=1, padx=5)

        # Add Entry button
        add_button = ttk.Button(entry_frame, text="Add Entry", command=lambda: add_entry(treeview, date_entry, description_entry))
        add_button.grid(row=2, column=0, pady=5)

        # Delete Entry button
        delete_button = ttk.Button(entry_frame, text="Delete Entry", command=lambda: delete_entry(treeview))
        delete_button.grid(row=2, column=1, padx=5, pady=5)

    def add_entry(treeview, date_entry, description_entry):
        date = date_entry.get()
        description = description_entry.get()
        if date and description:
            treeview.insert('', 'end', values=(date, description))
            date_entry.delete(0, tk.END)
            description_entry.delete(0, tk.END)

    def delete_entry(treeview):
        selected_item = treeview.focus()
        if selected_item:
            confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected entry?")
            if confirm:
                treeview.delete(selected_item)

    def open_transfer_window():
        transfer_window = tk.Toplevel(main_window)
        transfer_window.title("Transfer")
        transfer_window.geometry("300x100")

        username_label = ttk.Label(transfer_window, text="Username:")
        username_label.pack()

        username_entry = ttk.Entry(transfer_window)
        username_entry.pack()

        transfer_button = ttk.Button(transfer_window, text="Transfer", command=lambda: transfer(username_entry.get()))
        transfer_button.pack(pady=10)

    def transfer(username):
        messagebox.showinfo("Transfer", f"Transfer to user '{username}' successful.")

    # Create a frame for the list and buttons
    frame = ttk.Frame(main_window)
    frame.pack(padx=10, pady=10)

    # Create a scrollable treeview
    treeview = ttk.Treeview(frame, columns=("Vehicles",), show="headings")
    treeview.column("Vehicles", width=200)
    treeview.heading("Vehicles", text="Vehicles")
    treeview.bind('<<TreeviewSelect>>', select_item)
    treeview.pack(fill=tk.BOTH, expand=True)

    # Create buttons frame
    buttons_frame = ttk.Frame(main_window)
    buttons_frame.pack()

    # Create buttons
    add_vehicle_button = ttk.Button(buttons_frame, text="Add Vehicle", command=open_vehicle_window)
    add_vehicle_button.pack(side=tk.LEFT, padx=5)

    delete_vehicle_button = ttk.Button(buttons_frame, text="Delete Vehicle", command=delete_item)
    delete_vehicle_button.pack(side=tk.LEFT, padx=5)

    view_records_button = ttk.Button(buttons_frame, text="View Records", command=open_view_window)
    view_records_button.pack(side=tk.LEFT, padx=5)

    transfer_button = ttk.Button(buttons_frame, text="Transfer", command=open_transfer_window)
    transfer_button.pack(side=tk.LEFT, padx=5)

    main_window.mainloop()

# Create the login window
login_window = tk.Tk()
login_window.title("Auto Records Online")

# Username label and entry
username_label = tk.Label(login_window, text="Username:")
username_label.grid(row=0, column=0, sticky=tk.W)
username_entry = tk.Entry(login_window)
username_entry.grid(row=0, column=1)

# Password label and entry
password_label = tk.Label(login_window, text="Password:")
password_label.grid(row=1, column=0, sticky=tk.W)
password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1)

# Login button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.grid(row=2, column=0, padx=5, columnspan=2)

# Create button
create_button = tk.Button(login_window, text="Create", command=lambda: create_account(username_entry.get(), password_entry.get()))
create_button.grid(row=3, column=0, padx=5, columnspan=2)

login_window.mainloop()