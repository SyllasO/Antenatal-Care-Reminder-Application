import mysql.connector
from tkinter import messagebox
import tkinter as tk
from datetime import datetime


# Establish a connection to the MySQL server
def connect_db():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",  # MySQL server address (localhost for local machine)
            user="root",       # MySQL username
            password="Manners@0240",  # MySQL password
            database="antenatal_care"  # Use the antenatal_care database
        )
        return db_connection
    except mysql.connector.Error as err:
        messagebox.showerror("MySQL Error", f"Error: {err}")
        return None


# Function to create the database and tables if they don't exist
def create_database_and_tables():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",  # MySQL server address (localhost for local machine)
            user="root",       # MySQL username
            password="Manners@0240"  # MySQL password
        )
        
        cursor = db_connection.cursor()
        
        # Step 1: Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS antenatal_care;")
        cursor.execute("USE antenatal_care;")
        
        # Step 2: Create the Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone_number VARCHAR(15),
            role ENUM('patient', 'provider') NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            date_of_birth DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Step 3: Create the Appointments table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            appointment_date DATETIME NOT NULL,
            doctor_id INT,
            appointment_type ENUM('checkup', 'scan', 'test') NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (doctor_id) REFERENCES users(user_id)
        );
        """)
        
        # Step 4: Create the Reminders table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            reminder_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            appointment_id INT,
            reminder_date DATETIME NOT NULL,
            message TEXT NOT NULL,
            is_sent BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
        );
        """)
        
        # Step 5: Create the Health Data table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_data (
            health_data_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            checkup_date DATETIME NOT NULL,
            weight DECIMAL(5, 2),
            blood_pressure VARCHAR(50),
            blood_sugar DECIMAL(5, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """)
        
        # Step 6: Create the Patients table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            due_date DATE,
            reminder_time DATETIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        db_connection.commit()  # Commit the transaction
        cursor.close()  # Close the cursor
        db_connection.close()  # Close the connection
        messagebox.showinfo("Success", "Database and tables have been successfully created!")
    
    except mysql.connector.Error as err:
        messagebox.showerror("MySQL Error", f"Error: {err}")


# Function to insert a new patient into the database
def insert_patient(name, due_date, reminder_time):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Insert the patient data into the patients table
            insert_query = "INSERT INTO patients (name, due_date, reminder_time) VALUES (%s, %s, %s)"
            data = (name, due_date, reminder_time)
            cursor.execute(insert_query, data)
            conn.commit()
            messagebox.showinfo("Success", "Patient reminder saved successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()  # Always close the cursor
            conn.close()    # Always close the connection


# Create the main window for the GUI
root = tk.Tk()
root.title("Antenatal Care Reminder")

# Create the labels and entry fields for patient data
patient_name_label = tk.Label(root, text="Patient Name:")
patient_name_label.pack()
patient_name_entry = tk.Entry(root)
patient_name_entry.pack()

due_date_label = tk.Label(root, text="Due Date (MM-DD-YYYY):")
due_date_label.pack()
due_date_entry = tk.Entry(root)
due_date_entry.pack()

reminder_time_label = tk.Label(root, text="Reminder Time (MM-DD-YYYY HH:MM):")
reminder_time_label.pack()
reminder_time_entry = tk.Entry(root)
reminder_time_entry.pack()

# Function to handle the save button click
def on_save_button_click():
    patient_name = patient_name_entry.get()
    due_date = due_date_entry.get()
    reminder_time = reminder_time_entry.get()

    if patient_name and due_date and reminder_time:
        try:
            # Convert the dates into proper formats (This assumes the format input is valid)
            # You can add more validation for the date formats as necessary
            due_date_obj = datetime.strptime(due_date, "%m-%d-%Y").date()
            reminder_time_obj = datetime.strptime(reminder_time, "%m-%d-%Y %H:%M")

            # Save data to MySQL database
            insert_patient(patient_name, due_date_obj, reminder_time_obj)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid date format: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Input Error", "Please fill all fields correctly.")

# Create the save button
save_button = tk.Button(root, text="Save Reminder", command=on_save_button_click)
save_button.pack()

# Call the function to create the database and tables if they don't exist
create_database_and_tables()

# Run the main event loop
root.mainloop()
