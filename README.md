# Salary Management System

## Overview
The Salary Management System is a comprehensive web application designed to streamline the management of employee salary rates and attendance records. Built using Flask, a lightweight web framework, and SQL Server for data storage, this application provides a user-friendly interface that simplifies the complexities of payroll management.

With this system, administrators can easily manage employee data, calculate salaries based on hourly rates, and generate detailed reports. The application is particularly useful for businesses looking to automate their payroll processes, ensuring accuracy and efficiency while reducing the administrative burden.

## Features
- **User Authentication**: Secure login functionality to ensure that only authorized personnel can access sensitive employee data.
- **Manage Hourly Rates and Expenses**: Easily update and manage employee hourly rates and associated expenses, allowing for accurate payroll calculations.
- **View and Manage Employee Attendance**: Track employee attendance records, making it simple to monitor hours worked and calculate salaries accordingly.
- **Generate Salary Reports in PDF Format**: Create detailed salary reports that can be exported as PDFs, making it easy to share and review payroll information.

## Screenshot
Below is a screenshot of the application interface:
![Screenshot](https://github.com/user-attachments/assets/0c88484f-7099-4607-abfb-99a0608673ea)

## Requirements
To run the Salary Management System, you will need the following software installed on your machine:
- **Python 3.x**: The programming language used to build the application.
- **Flask**: A lightweight web framework for Python that allows for rapid development of web applications.
- **Flask-SocketIO**: A Flask extension that enables real-time communication between the server and clients.
- **pyodbc**: A Python library that provides an interface to connect to SQL Server databases.

### `requirements.txt`
```
Flask
Flask-SocketIO
pyodbc
```

## Installation
To set up the Salary Management System on your local machine, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/YA195/Salary.git
   cd Salary
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application:
```bash
python app.py
```
Navigate to [http://localhost:5001](http://localhost:5001) in your web browser to access the application.

## API Endpoints
- `GET /get_names`: Retrieve a list of employee names.
- `GET /get_rates`: Retrieve current salary rates and expenses.
- `POST /update_rate`: Update or add a salary rate for an employee.
- `GET /get_attendance`: Retrieve attendance records for an employee within a date range.
- `GET /get_all_attendance`: Retrieve attendance records for multiple employees within a date range.

## License
This project is licensed under the MIT License.

## Acknowledgments
- Flask documentation for guidance on building web applications.
- Bootstrap for styling the user interface.
