import sqlite3
from datetime import date, datetime, timedelta

def get_db(name="main.db"): # Connects to a SQLite databe, creating necessary tables in the DB and then returns the database connection
    db = sqlite3.connect(name)
    create_tables(db)
    return db

def create_tables(db): # Defines and Creates tables
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS counter (
        name TEXT PRIMARY KEY,
        description TEXT,
        periodicity TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
        date TEXT,
        counterName TEXT,
        FOREIGN KEY (counterName) REFERENCES counter(name))""")

    db.commit()

def add_counter(db, name, description, periodicity): # Stores this data to the "counter" table
    cur = db.cursor()
    cur.execute("INSERT INTO counter VALUES (?, ?, ?)", (name, description, periodicity))
    db.commit()

def increment_counter(db, name, event_date=None): # Stores this data to the "tracker" table
    cur = db.cursor()
    if not event_date: # If no date is provided, it will save the current date
        event_date = str(date.today())
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, name))
    db.commit()

def get_counter_data(db, name): # selects all data from "tracker" table for a specific habit
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE counterName=?", (name,))
    return cur.fetchall()



def get_periodicity(db, name): # selects the periodicity from "counter" table for a specific habit
    cur = db.cursor()
    cur.execute("SELECT periodicity FROM counter WHERE name=?", (name,))
    return cur.fetchall()[0][0]

def get_countername_list(db): # returns a list (without duplicates) from "counter" table with all the habits
    cur = db.cursor()
    cur.execute("select name from counter")
    all_counters = cur.fetchall()
    counters_set = set()
    for counters in all_counters:
        counters_set.add(counters[0])
    return list(counters_set)

def get_counternameper_list(db, periodicity): # returns a list (without duplicates) of habits from "counter" table for a specific periodicity
    cur = db.cursor()
    cur.execute("select name from counter WHERE periodicity=?", (periodicity,))
    all_periodicity = cur.fetchall()
    periodicity_set = set()
    for periodicity in all_periodicity:
        periodicity_set.add(periodicity[0])
    return list(periodicity_set)



def single_habit_cut_list(db, name): # returns a sorted list (without duplicates) from "tracker" table with all incrementation dates for a habit
    cur = db.cursor()
    cur.execute("select * from tracker WHERE counterName=?", (name,))
    all_dates = cur.fetchall()
    date_set = set()
    for date in all_dates:
        date_set.add(datetime.strptime(date[0], '%Y-%m-%d').date())
    return sorted(list(date_set))


def habit_dates(db, name): # all dates per habit
    cur = db.cursor()
    cur.execute("select date from tracker WHERE counterName=?", (name,))
    all_dates = cur.fetchall()
    date_set = set()
    for date in all_dates:
        date_set.add(date[0])
    return sorted(list(date_set))

def habit_weeks(db, name): # all weeks per habit
    cur = db.cursor()
    cur.execute("select * from tracker WHERE counterName=?", (name,))
    all_dates = cur.fetchall()
    date_set = set()
    for date in all_dates:
        temp = (datetime.strptime(date[0], '%Y-%m-%d').date())
        date_set.add(temp.isocalendar()[1])
    return sorted(list(date_set))



def delete_counter(db, name): # deletes data from "tracker" and "counter" tables for a specific habit
    cur = db.cursor()
    cur.execute("DELETE from tracker WHERE counterName=?", (name,))
    cur.execute("DELETE from counter WHERE name=?", (name,))
    db.commit()

def previous_days():
    date_list = []
    for x in range(5):
        date_list.append(str(date.today()-timedelta(x)))
    return date_list[::-1]

def previous_weeks():
    week_numbers = []
    for x in range(5):
        current_date = date.today() - timedelta(weeks=x)
        week_number = current_date.isocalendar()[1]
        week_numbers.append(week_number)
    return week_numbers[::-1]



