# 📊 BitFutura Employee Management System (EMS)

A Python-based command-line **Employee Management System** designed for SMEs and HR departments to manage employees efficiently. The system supports adding, updating, viewing, deleting, and reporting employee records with built-in data validation and email notifications.

---

## 🧠 Project Overview

This project was developed as part of the PDWD-PFS-0325 software engineering coursework. It emphasizes object-oriented programming principles, user validation, CSV file persistence, and unit-tested logic.

---

## 🚀 Features

- ✅ Add new employees with email confirmation  
- 🔍 View employee details by ID  
- ✏️ Update employee information with two-step validation  
- ❌ Delete employee records with double confirmation  
- 📋 List all employees with structured formatting  
- 📊 Generate department-wise reports including salary budget  
- 📬 Sends confirmation emails using SMTP (modularized via `send_email.py`)  

---

## 🏗️ Project Structure

```
├── BitFutura_Employee_Management_System.py    # Main EMS logic
├── send_email.py                              # Handles sending email via SMTP
├── employees.csv                              # CSV file for storing employee data
├── test_employee_management.py                # Unit tests using unittest + mock
├── README.md                                  # Project documentation
```

---

## 🧩 Core Classes & Methods

| Class | Description |
|-------|-------------|
| `Employee` | Represents an individual employee. Attributes: `emp_id`, `name`, `department`, `salary`, `contact`. |
| `EmployeeManagementSystem` | Manages a list of `Employee` objects and provides methods to add, update, delete, and list employees. |

**Main Functional Methods:**
- `add_employee()` – Add new employee with input prompts and validations
- `update_employee()` – Edit employee record (supports partial update)
- `delete_employee()` – Remove an employee after double confirmation
- `view_employee()` – View employee details using ID
- `list_all_employees()` – Show all employees in the system
- `department_wise_report()` – Report employees grouped by department and total salary

---

## 🧪 Unit Testing

Automated tests are written using `unittest`, `mock`, and `StringIO` to simulate:
- Input validation
- Employee creation and search
- Update and delete workflows
- Department-wise reporting

To run tests:

```bash
python test_employee_management.py
```

---

## 📧 Email Notification Setup

This project uses `send_email.py` to dispatch confirmation emails upon employee addition.

**Setup Gmail SMTP (Recommended):**
1. Enable 2FA in your Gmail account.
2. Generate an App Password.
3. Replace credentials in the constructor:

```python
self.email_sender = EmailSender("your_email@gmail.com", "your_app_password")
```

> Note: This uses `smtplib` and `email.mime` internally.

---

## ✅ Sample Validation Rules

| Field | Rule |
|-------|------|
| Employee ID | Must start with 'E' followed by 8 digits (`E12345678`) |
| Name | Alphabets + space, max 20 characters |
| Department | Alphabets only, max 20 characters |
| Salary | Digits only |
| Contact | Valid email format, max 20 characters |

---

## 💾 File Persistence

- All data is stored in `employees.csv`
- Headers: `ID, Name, Department, Salary, Contact`
- CSV operations are handled using Python’s built-in `csv` module.

---

## 📜 How to Run

```bash
python BitFutura_Employee_Management_System.py
```

You’ll see a menu:
```
1. Add Employee
2. View Employee
3. Update Employee
4. Delete Employee
5. List All Employees
6. Department Wise Report
7. Exit
```

---

## 🛡️ Error Handling

- Graceful error messages for file I/O
- Validation for duplicates, bad formats
- Confirmation prompts before critical actions

---

## 🧠 Designed By

**Tan Wesley**  
Coursework Submission – *PDWD-PFS-0325-Summative Assessment*  
