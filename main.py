import tkinter as tk
import ttkbootstrap as tb
from db import get_db, get_countername_list, get_counternameper_list, previous_days, previous_weeks, habit_dates, habit_weeks
from counter import Counter
from analyse import calculate_streak

def gui():
    db = get_db()

    def dashboard_frame():
        # Remove any existing content in the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()
        # Add the new content to the right frame
        name_frame = tb.Frame(right_frame)
        name_frame.pack(padx=50)

        #-------------------------------Daily
        tb.Label(right_frame, text= "Daily Habits", font= ("Helvetica", 14, "bold")).pack(pady=10)

        # Fills dates at top
        daily_frame = tb.Frame(right_frame)
        tb.Label(daily_frame, text="Date:", width=8, font= ("Helvetica", 10, "bold")).pack(pady=10, side = "left")
        for day in previous_days():
            tb.Label(daily_frame, text=day, font=("Helvetica", 10, "bold")).pack(padx=8, pady=10, side="left")
        daily_frame.pack(anchor="w")
        tb.Label(daily_frame, text="Longest Streak", font=("Helvetica", 10, "bold")).pack(pady=10, side="left")

        # Fills the habit's accomplishment
        for habit in get_counternameper_list(db, "Daily"):
            habit_frame = tb.Frame(right_frame)
            tb.Label(habit_frame, text = habit, width=10).pack(pady=10, side="left")
            for day in previous_days():
                if day in habit_dates(db, habit):
                    tb.Frame(habit_frame, width=83, height= 20, bootstyle="success").pack(pady=10, side="left")
                else:
                    tb.Frame(habit_frame, width=83, height= 20, bootstyle="danger").pack(pady=10, side="left")
            try:
                streak = calculate_streak(db, habit)[0]
                streak_width = streak*65/365
                tb.Frame(habit_frame, width=streak_width, height= 20, bootstyle="success").pack(padx=10, pady=10, side="left")
                tb.Label(habit_frame, text=streak, font=("Helvetica", 10, "bold")).pack(pady=10, side="left")
            except (ValueError):
                tb.Label(habit_frame, text="0", font=("Helvetica", 10, "bold")).pack(padx=10, pady=10, side="left")
            habit_frame.pack(anchor="w")

        #-------------------------------Weekly
        tb.Label(right_frame, text="Weekly Habits", font= ("Helvetica", 14, "bold")).pack(pady=10)

        # Fills week numbers at top
        weekly_frame = tb.Frame(right_frame)
        tb.Label(weekly_frame, text="Week:", width=8, font= ("Helvetica", 10, "bold")).pack(pady=10, side = "left")
        for day in previous_weeks():
            tb.Label(weekly_frame, text=day, font=("Helvetica", 10, "bold")).pack(padx=33, pady=10, side="left")
        weekly_frame.pack(anchor="w")
        tb.Label(weekly_frame, text="Longest Streak", font=("Helvetica", 10, "bold")).pack(pady=10, side="left")

        # Fills the habit's accomplishment
        for habit in get_counternameper_list(db, "Weekly"):
            habit_frame = tb.Frame(right_frame)
            tb.Label(habit_frame, text = habit, width=10).pack(pady=10, side="left")
            for week in previous_weeks():
                if week in habit_weeks(db, habit):
                    tb.Frame(habit_frame, width=83, height=20, bootstyle="success").pack(pady=10, side="left")
                else:
                    tb.Frame(habit_frame, width=83, height=20, bootstyle="danger").pack(pady=10, side="left")
            try:
                streak = calculate_streak(db, habit)[0]
                streak_width = streak * 65 / 52
                tb.Frame(habit_frame, width=streak_width, height= 20, bootstyle="success").pack(padx=10, pady=10, side="left")
                tb.Label(habit_frame, text = streak, font=("Helvetica", 10, "bold")).pack(pady=10, side="left")
            except (ValueError):
                tb.Label(habit_frame, text="0", font=("Helvetica", 10, "bold")).pack(padx=10, pady=10, side="left")
            habit_frame.pack(anchor="w")

    def create_habit_frame():
        # Remove any existing content in the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()
        # Add the new content to the right frame
        name_frame = tb.Frame(right_frame)
        name_frame.pack(padx=50)

        # stringVars variables
        name_var = tk.StringVar()
        description_var = tk.StringVar()
        periodicity_var = tk.StringVar()


        # Function to be called when the Combobox selection changes
        def on_combobox_select(event):
            periodicity_var.set(periodicity_combobox.get())

        # Habit Name
        tb.Label(name_frame, text = "Habit's Name:", width=17).pack(pady=10,side="left")
        name_entry = tb.Entry(name_frame, width=15, textvariable=name_var)
        name_entry.pack(expand=True, padx=10, pady=10, side="left")

        # Habit Description
        description_frame = tb.Frame(right_frame)
        description_frame.pack()
        tb.Label(description_frame, text="Habit's Description:", width=17).pack(pady=10, side="left")
        description_entry = tb.Entry(description_frame, width=15, textvariable=description_var)
        description_entry.pack(expand=True, padx=10, pady=10, side="left")

        # Habit Periodicity
        periodicity_frame = tb.Frame(right_frame)
        periodicity_frame.pack()
        tb.Label(periodicity_frame, text="Habit's Periodicity:", width=17).pack(pady=10, side="left")
        periodicity_combobox = tb.Combobox(periodicity_frame, width=13, values=["Daily", "Weekly"], textvariable=periodicity_var)
        periodicity_combobox.pack(expand=True, padx=10, pady=10, side="left")
        periodicity_combobox.bind("<<ComboboxSelected>>", on_combobox_select)

        def create_new_habit():
            if name_var.get() and description_var.get() and periodicity_var.get():
                name = name_entry.get()
                desc = description_entry.get()
                per = periodicity_combobox.get()
                counter = Counter(name, desc, per)
                counter.store(db)
                create_habit_frame()
            else:
                pass

        tb.Button(right_frame, text="Create", width=40, bootstyle="primary, outline", command= create_new_habit).pack(
            expand=True, pady=10)


    def increment_habit_frame():
        # Remove any existing content in the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()
        # Add the new content to the right frame
        increment_frame = tb.Frame(right_frame)
        increment_frame.pack(padx=50)

        # stringVars variables
        name = tk.StringVar()

        tb.Label(increment_frame, text="Habit to Increment:", width=17).pack(pady=10, side="left")

        def on_combobox_select(event):
            name.set(combobox.get())

        combobox = tb.Combobox(increment_frame, width=13, values=get_countername_list(db))
        combobox.pack(expand=True, padx=10, pady=10, side="left")

        combobox.bind("<<ComboboxSelected>>", on_combobox_select)

        def increment_selected_habit():
            selected_name = name.get()
            counter = Counter(selected_name, "no description", "no periodicity")
            counter.increment()
            counter.add_event(db)
            increment_habit_frame()

        # Create the "Create" button initially disabled
        create_button = tb.Button(right_frame, text="Increment", width=40, bootstyle="primary, outline", command= increment_selected_habit)
        create_button.pack(expand=True, pady=10)

    def delete_habit_frame():
        # Remove any existing content in the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()
        # Add the new content to the right frame
        periodicity_frame = tb.Frame(right_frame)
        periodicity_frame.pack(padx=50)
        # stringVars variables
        name = tk.StringVar()

        tb.Label(periodicity_frame, text="Habit to Delete:", width=17).pack(pady=10, side="left")

        def on_combobox_select(event):
            name.set(combobox.get())

        combobox = tb.Combobox(periodicity_frame, width=13, values=get_countername_list(db))
        combobox.pack(expand=True, padx=10, pady=10, side="left")

        combobox.bind("<<ComboboxSelected>>", on_combobox_select)

        # Define a function to delete the selected habit
        def delete_selected_habit():
            selected_name = name.get()
            counter = Counter(selected_name, "no description", "no periodicity")
            counter.delete_habit(db)
            delete_habit_frame()

        tb.Button(right_frame, text="Delete", width=40, bootstyle="primary, outline", command=delete_selected_habit).pack(
            expand=True, pady=10)





    # Window
    root = tb.Window(themename="solar")
    root.title("Habit Tracking App")
    root.geometry("800x600")
    themes = root.style.theme_names()
    theme = tb.StringVar(value=root.style.theme_use())


    # ---------------------------------------Left Frame
    left_frame = tb.Frame(root, width=200, height= 600, bootstyle="dark")
    left_frame.pack(anchor="nw", expand=True, fill="y")


    def on_combobox_select(event):
        root.style.theme_use(theme.get())


    # Buttons
    tb.Button(left_frame, text ="Dashboard", width=16, bootstyle = "primary", command=dashboard_frame).pack(padx=24,pady=10, side="top")
    tb.Button(left_frame, text ="Create Habit", width=16, bootstyle = "primary", command=create_habit_frame).pack(padx=24,pady=10,side="top")
    tb.Button(left_frame, text ="Increment Habit", width=16, bootstyle = "primary", command=increment_habit_frame).pack(padx=24,pady=10,side="top")
    tb.Button(left_frame, text ="Delete Habit", width=16, bootstyle = "primary", command=delete_habit_frame).pack(padx=24,pady=10,side="top")
    theme_combobox = tb.Combobox(left_frame, width=16, values=themes, textvariable=theme)
    theme_combobox.pack(padx=24, pady=10, side="bottom")
    theme_combobox.bind("<<ComboboxSelected>>", on_combobox_select)



    # ---------------------------------------Right Frame
    right_frame = tb.Frame(root)
    right_frame.place(x=200, y=0, anchor="nw")



    # Pack the initial content into the right frame


    # Run
    root.mainloop()


if __name__ == "__main__":
    gui()