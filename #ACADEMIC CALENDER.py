#ACADEMIC CALENDER
""" Academic Scheduler """

import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import json
import customtkinter as ctk
from datetime import datetime
from plyer import notification

file_name = "user's_planner_data.txt" # This is the file used to save the tasks

#  A dict() to enter and store user details
data = {
    "Academic_Year": "1st Year",
    "Semester": "1st Sem",
    "todos": []
}
# -1 means no task is being edited, otherwise it will be the index of the task being edited
edit_id = -1

# This function will allow the system to store the created dict to the file
def save_data():
    """ Save the data to the file """
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    """ Read the old data and load the data from the file """
    try:
        with open(file_name, "r") as file:
            data.update(json.load(file))
    except FileNotFoundError:
        save_data()  # Create the file if it doesn't exist

# This function is defined to clear the user's latest details 
def clear_data():
    name_data.delete(0, "end")
    time_data.delete(0, "end")
    error_data.configure(text="")  # Clear the error message

def save_task():
    """ Save the task to the dictionary and file """
    global edit_id
    # The users will have to enter their info into this required input field
    name = name_data.get().strip()
    due = time_data.get().strip()

    # All the entries for user info must be filled or it won't proceed and display the same in the main screen
    if name == "" or due == "":
        error_data.configure(text="Please fill in all fields.")
        return
    
    # This validates the due date format 
    try:
        datetime.strptime(due, "%H:%M %d-%m-%Y")  # Validate the date format
    except ValueError:
        error_data.configure(text="Invalid date format. Use HH:MM DD-MM-YYYY.")
        return

    if edit_id != -1:
        # Find the task with the given edit_id and update its name and due date
        for task in data["todos"]:
            if task["id"] == edit_id:
                task["name"] = name
                task["due"] = due
                task["warned_urgent"] = False  
                task["warned_today"] = False
        # editing is done, reset edit_id and change button text back to "Add Task"
        edit_id = -1  
        add_btn.configure(text="Add Task", fg_color="#3b82f6")

    else:
        # A task is stored as a dictionary with name, due date, unique ID, and status
        task = {
            "name": name,
            "id": int(datetime.now().timestamp()),  # Unique ID based on timestamp
            "due": due,
            "status": "pending",  # Default status is pending
        }
        data["todos"].append(task)  # Add the new task to the list
    # It saves and keep updating the list after every change in the loop
    save_data()  
    clear_data() 
    show_tasks() 

def edit_task(task_id, name, due):
    """ Put the task data in the input fields for editing """
    global edit_id

    edit_id = task_id
    name_data.delete(0, "end")
    name_data.insert(0, name)
    time_data.delete(0, "end")
    time_data.insert(0, due)
    add_btn.configure(text="Save Changes", fg_color="#f59e0b")  

def del_task(task_id):
    """ Delete a task from the list """
    global edit_id

    # Make a new list of tasks excluding the one with the given task_id
    new_tasks = []
    for task in data["todos"]:
        if task["id"] != task_id:
            new_tasks.append(task)
    data["todos"] = new_tasks

    # If the task being deleted is currently being edited, reset edit_id and change button text back to "Add Task"
    if edit_id == task_id:
        edit_id = -1
        add_btn.configure(text="Add Task", fg_color="#3b82f6")

    save_data()  
    show_tasks() 

def save_choices():
    """ Save the academic year and semester choices to the dictionary and file """
    data["Academic_Year"] = year_data.get()
    data["Semester"] = sem_data.get()
    save_data()  

# It will display all the saved tasks on the right side of the popped up dashboard in the main screen
def show_tasks():
    # It will first remove the old rows so that the list can be updated accordingly
    for i in task_area.winfo_children():
        i.destroy()

    now = datetime.now()

    # This Checks every task one by one in a sequence
    for task in data["todos"]:
        BackGround = "#374151"
        text_colour = "white"
        status = "PENDING"

        try:
            due = datetime.strptime(task["due"], "%H:%M %d-%m-%Y")
            left = (due - now).total_seconds()

            # A task whose time has passed is declared missed
            if now > due:
                BackGround = "#451a03"
                text_colour = "#f87171"
                status = "MISSED"

            # A task due within one hour is urgent
            elif left <= 3600:
                BackGround = "#2d1500"
                text_colour = "#fbbf24"
                status = "URGENT"

            # A task due later today gets the TODAY status   
            elif due.date() == now.date():
                BackGround = "#1e3a8a"
                text_colour = "#60a5fa"
                status = "TODAY"
        except ValueError:
            pass # Invalid dates are ignored here because input was checked earlier

        # This uses ne frame as one task row 
        row = ctk.CTkFrame(
            task_area,
            fg_color = BackGround,
            corner_radius = 6
        )
        row.pack(padx=5, pady=3, fill="x")

        # It displays the task name, deadline and the status...
        ctk.CTkLabel(
            row,
            text=f"{task['name']} | Due: {task['due']} ({status})",
            font=("Arial", 11, "bold"),
            text_color=text_colour
        ).pack(side="left", padx=10, pady=6)

        # X deletes the task.
        ctk.CTkButton(
            row,
            text="X",
            width=25,
            height=22,
            fg_color="#ef4444",
            command=lambda x=task["id"]: del_task(x)
        ).pack(side="right", padx=6, pady=6)         

        ctk.CTkButton(
            row,
            text="Edit",
            width=40,
            height=22,
            fg_color="#f59e0b",
            command=lambda x=task["id"], n=task["name"], d=task["due"]:
            edit_task(x, n, d)
        ).pack(side="right", padx=3, pady=6)

# It Checks deadlines repeatedly in the background to give the status in notification panel
# It Checks deadlines repeatedly in the background to give the status in notification panel
def verify_deadlines():
    now = datetime.now()
    changed = False
    for task in data["todos"]:
        # Only the unfinished tasks would process the deadline checking
        if task.get("status") != "pending":
            continue

        try:
            due = datetime.strptime(task["due"], "%H:%M %d-%m-%Y")
            left = (due - now).total_seconds()
            
            if now > due:
                task["status"] = "missed"
                changed = True
                os.system("afplay /System/Library/Sounds/Basso.aiff &") 
                # Native macOS Notification
                os.system(f"""osascript -e 'display notification "{task['name']}" with title "Missed!"'""")
                
            elif left <= 3600 and not task.get("warned_urgent"):
                task["warned_urgent"] = True
                changed = True
                os.system("afplay /System/Library/Sounds/Glass.aiff &") 
                # Native macOS Notification
                os.system(f"""osascript -e 'display notification "{task['name']} due soon" with title "Urgent!"'""")
                
            elif due.date() == now.date() and not task.get("warned_today"):
                task["warned_today"] = True
                changed = True
                os.system("afplay /System/Library/Sounds/Pop.aiff &") 
                # Native macOS Notification
                os.system(f"""osascript -e 'display notification "{task['name']}" with title "Today!"'""")
                
        except ValueError:
            pass

    # It saves only when something is changed.
    if changed:
        save_data()
        show_tasks()

    # This help run this function again after 10 seconds.
    root.after(10000, verify_deadlines)



# The login and registration panel before accessing the dashboard use the same simple input.
def login():
    user = user_data.get().strip()

    if user != "":
        data["student_info"] = user
        save_data()
        login_frame.pack_forget()
        main_screen()        

# Change the login screen into the registration screen and back.
def change_login(event):
    if "Sign Up" in switch_label.cget("text"):
        heading.configure(text="Register Account")
        login_btn.configure(text="Register")
        switch_label.configure(text="Have an account? Login")
    else:
        heading.configure(text="Welcome to Study Planner")
        login_btn.configure(text="Login")
        switch_label.configure(text="Don't have an account? Sign Up")

# This creates the main planner screen.
def main_screen():
    global name_data, time_data, error_data
    global add_btn, year_data, sem_data, task_area

    # The window-dashboard will have two main columns for the user.
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=2)
    root.grid_rowconfigure(0, weight=1)

    # The left side of the dashboard will allow user to help access the input controls.
    left = ctk.CTkFrame(root, fg_color="#1f2937")
    left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    ctk.CTkLabel(
        left,
        text=f"User: {data.get('student_info')}",
        text_color="#60a5fa",
        font=("Arial", 13, "bold")
    ).pack(padx=10, pady=10, anchor="w")

    # User can select the academic year
    year_data = ctk.CTkComboBox(
        left,
        values=["1st Year", "2nd Year", "3rd Year", "4th Year"],
        command=save_choices
    )
    year_data.pack(padx=10, pady=4, fill="x")
    year_data.set(data.get("Academic_Year", "1st Year"))

    # Semester is selected by the user.
    sem_data = ctk.CTkComboBox(
        left,
        values=["1st Sem", "2nd Sem"],
        command=save_choices
    )
    sem_data.pack(padx=10, pady=4, fill="x")
    sem_data.set(data.get("Semester", "1st Sem"))

    # User's filled in Task name and deadline is scheduled
    name_data = ctk.CTkEntry(left, placeholder_text="Task Name")
    name_data.pack(padx=10, pady=4, fill="x")

    time_data = ctk.CTkEntry(left, placeholder_text="HH:MM DD-MM-YYYY")
    time_data.pack(padx=10, pady=4, fill="x")

    error_data = ctk.CTkLabel(left, text="", text_color="#f87171")
    error_data.pack(padx=10, pady=1, anchor="w")

    add_btn = ctk.CTkButton(left, text="Add Task", command=save_task)
    add_btn.pack(padx=10, pady=6, fill="x")

    ctk.CTkButton(
        left,
        text="Clear",
        fg_color="#4b5563",
        command=clear_data
    ).pack(padx=10, pady=4, fill="x")

    # Right side of the dashboard displays the saved tasks.
    right = ctk.CTkFrame(root, fg_color="#111827")
    right.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")

    task_area = ctk.CTkScrollableFrame(
        right,
        label_text="Scheduled Tasks List",
        fg_color="#1f2937"
    )
    task_area.pack(padx=15, pady=15, fill="both", expand=True)

    show_tasks()
    verify_deadlines()      

"""*******************************PROGRAM STARTS HERE******************************"""

load_data()
# These two lines set the appearance of the CustomTkinter window.
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Creates the main application window.
root = ctk.CTk()
root.title("Study Planner")
root.geometry("900x580")
root.resizable(False, False)

# This frame will be displayed before the main planner is shown.
login_frame = ctk.CTkFrame(
    root,
    width=380,
    height=300,
    fg_color="#1f2937"
)
login_frame.pack(expand=True)

heading = ctk.CTkLabel(
    login_frame,
    text="Welcome to Study Planner",
    font=("Arial", 18, "bold")
)
heading.pack(padx=20, pady=15)
user_data = ctk.CTkEntry(
    login_frame,
    placeholder_text="Enter Username details",
    width=260
)
user_data.pack(padx=20, pady=8)
login_btn = ctk.CTkButton(
    login_frame,
    text="Login",
    command=login
)
login_btn.pack(padx=20, pady=12)
switch_label = ctk.CTkLabel(
    login_frame,
    text="Don't have an account? Sign Up",
    text_color="#60a5fa",
    cursor="hand2"
)
switch_label.pack(padx=20, pady=8)
switch_label.bind("<Button-1>", change_login)

# If a username already exists, it skip the login screen.
if data.get("student_info"):
    login_frame.pack_forget()
    main_screen()

# Here, finally the the GUI processes.
root.mainloop()