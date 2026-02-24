# Teledex – Desktop Telemetry & Analytics Engine App

**Portfolio project for an Entry-Level Backend Developer position**

## 🚀 Overview

Teledex is a sticky-note style desktop gui app for general office use with these features:
--A 3 column x 3 row user input/display field as follows: 
    > Column 1 allows user to make a label/title for each row.  
    > Column 2 displays "0" by default. Clicking adjacent "UPDATE" icon increments by 1.  Otherwise, can click directly on the input box and enter custom entry.   
    > Column 3 displays "PLOT" button icons for displaying plots for each row of entries. Clicking changes plot by month, week, then day. Plots are displayed in a pop-up window to the left, top, or right of the gui icon for rows 1, 2, or 3 respectively. Clicking again retracts plot back into app.     
--A weather display with current weather and rain prediction on the gui for convenience.
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

## 📌 Future Enhancements

- --A 3 x 1 row user input/display field comprising: 
    > database name: Displays current database name. Click to change.
    > timestamp: Display time of entry.
    > security: Displays enterer's name. Requests security code if secure database entered in column 1. 
- Android version
- Combine plots onto one plot.  


## Download and Run Teledex on Your Desktop

Follow these steps to try Teledex:

1. **Clone the repository**

Open a terminal or command prompt and run:

```bash
git clone https://github.com/yourusername/teledex.git
cd teledex
