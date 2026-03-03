# Teledex – Desktop Telemetry & Analytics Engine App

**Portfolio project for an Entry-Level Backend Developer position**

## 🚀 Overview

Teledex is a sticky-note style desktop gui app for general office use with these features:
--A 3 column x 3 row user input/display field as follows: 
    > Column 1 allows user to make a label/title for each row.  
    > Column 2 displays "0" by default. Clicking adjacent "UPDATE" icon increments by 1.  Otherwise, can click directly on the input box and enter custom entry.   
    > Column 3 displays "PLOT" button icons for displaying plots for each row of entries. Clicking changes plot by month, week, then day. Plots are displayed in a pop-up window to the left, top, or right of the gui icon for rows 1, 2, or 3 respectively. Clicking again retracts plot back into app.     
--A weather display with current weather and rain prediction on the gui for convenience.
--A button for interactive Python quizzes I made for practice.  Topics include:
    > @decorators
* More features will be added as this project is developed.  

## 📊 Example Use Case

--Flower shop sales. Input "roses" for row 1, "tulips" for row 2, "orchids" for row 3. Record each sale by clicking the UPDATE icon or enter manually using keyboard. Click plot to see graphs for month, week, or day with each click.  Roses on the left, tulips on top, orchids to the right.    
--Blood pressure record.  Row 1 for systolic. Enter 120 at 6am. Enter 130 at 6pm. Next day, enter 100 at 9am. Etc. Row 2 for diastolic. Enter 80 at 6am. Enter 70 at 6pm. Next day, enter 75 at 9am. Click plot to graph by month, week, then day with each click.  

## 🏗 Architecture

```
Tkinter UI
     ↓
Python Backend
     ↓
Supabase (PostgreSQL)
     ↓
Matplotlib Visualization
```
## SQL Practice Module

Teledex includes a lightweight SQL learning practice tool.

Features:
- In-memory SQLite training database
- 5 SQL exercises covering: SELECT queries, WHERE filtering, JOIN operations, GROUP BY aggregation
- Result validation engine

Run practice mode:

```bash
python run_sql_practice.py
```
## 📌 Future Enhancements

- --A 3 x 1 row user input/display field comprising: 
    > database name: Displays current database name. Click to change.
    > timestamp: Display time of entry.
    > security: Displays enterer's name. Requests security code if secure database entered in column 1. 
- Android version
- Combine plots onto one plot.  

## Download Teledex

Clone the repository:

```bash
git clone https://github.com/hansemso/teledex.git
cd teledex
```
## Run Teledex

After cloning the repository, run the application using Python:

```bash
py teledex_gui.py
```