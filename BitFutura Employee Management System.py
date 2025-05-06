import smtplib
from email.message import EmailMessage

# -------------------------------
# Entity Classes
# -------------------------------

class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, emp):
        self.employees.append(emp)

    def get_employee(self, emp_id):
        return next((e for e in self.employees if e.id == emp_id), None)

    def remove_employee(self, emp_id):
        self.employees = [e for e in self.employees if e.id != emp_id]

    def generate_report(self):
        print(f"\n📋 Department Report: {self.name}")
        print("-" * 50)
        print("{:<10} {:<20} {:<10}".format("ID", "Name", "Salary"))
        for emp in self.employees:
            print("{:<10} {:<20} ${:<10.2f}".format(emp.id, emp.name, emp.salary))
        print("-" * 50)


class Employee:
    def __init__(self, emp_id, name, department, salary, contact):
        self.id = emp_id
        self.name = name
        self.department = department
        self.salary = salary
        self.contact = contact

# -------------------------------
# Email Service
# -------------------------------

class EmailService:
    def __init__(self):
        self.sender_email = "wt.wn01@gmail.com"
        self.sender_password = "your-app-password-here"  # Replace with Gmail App Password

    def send_confirmation(self, recipient, name, department):
        try:
            subject = "Welcome to BitFutura"
            body = f"""Dear {name},

Welcome to the {department} department at BitFutura!
We are excited to have you on board.

Regards,
BitFutura HR Team
"""

            msg = EmailMessage()
            msg.set_content(body)
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            print(f"✅ Confirmation email sent to {recipient}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")

# -------------------------------
# EMS Controller Class
# -------------------------------

class EmployeeManagementSystem:
    def __init__(self):
        self.departments = {}
        self.email_service = EmailService()

    def get_or_create_department(self, name):
        if name not in self.departments:
            self.departments[name] = Department(name)
        return self.departments[name]

    def add_employee(self):
        try:
            emp_id = input("Enter Employee ID: ").strip()
            name = input("Enter Name: ").strip()
            dept_name = input("Enter Department: ").strip()
            salary = float(input("Enter Salary: ").strip())
            contact = input("Enter Contact Email: ").strip()

            dept = self.get_or_create_department(dept_name)
            if dept.get_employee(emp_id):
                print("⚠️ Employee ID already exists.")
                return

            emp = Employee(emp_id, name, dept, salary, contact)
            dept.add_employee(emp)
            print(f"✅ Employee {name} added.")

            self.email_service.send_confirmation(contact, name, dept_name)

        except ValueError:
            print("❌ Invalid salary. Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def view_employee(self):
        emp_id = input("Enter Employee ID to view: ").strip()
        for dept in self.departments.values():
            emp = dept.get_employee(emp_id)
            if emp:
                print(f"🔍 ID: {emp.id}, Name: {emp.name}, Dept: {emp.department.name}, Salary: ${emp.salary:.2f}, Email: {emp.contact}")
                return
        print("⚠️ Employee not found.")

    def update_employee(self):
        emp_id = input("Enter Employee ID to update: ").strip()
        for dept in self.departments.values():
            emp = dept.get_employee(emp_id)
            if emp:
                emp.name = input(f"New name [{emp.name}]: ") or emp.name
                try:
                    salary_input = input(f"New salary [{emp.salary}]: ")
                    if salary_input:
                        emp.salary = float(salary_input)
                except ValueError:
                    print("❌ Invalid salary input.")
                emp.contact = input(f"New email [{emp.contact}]: ") or emp.contact
                print("✅ Employee updated.")
                return
        print("⚠️ Employee not found.")

    def delete_employee(self):
        emp_id = input("Enter Employee ID to delete: ").strip()
        for dept in self.departments.values():
            if dept.get_employee(emp_id):
                dept.remove_employee(emp_id)
                print("✅ Employee deleted.")
                return
        print("⚠️ Employee not found.")

    def list_all_employees(self):
        print("\n👥 List of All Employees:")
        for dept in self.departments.values():
            for emp in dept.employees:
                print(f" - ID: {emp.id}, Name: {emp.name}, Dept: {emp.department.name}, Salary: ${emp.salary:.2f}, Email: {emp.contact}")

    def generate_department_reports(self):
        for dept in self.departments.values():
            dept.generate_report()

# -------------------------------
# CLI Application Runner
# -------------------------------

def run():
    system = EmployeeManagementSystem()

    while True:
        print("\n===== BitFutura EMS Menu =====")
        print("1. Add Employee")
        print("2. View Employee")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. List All Employees")
        print("6. Department-wise Report")
        print("7. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            system.add_employee()
        elif choice == "2":
            system.view_employee()
        elif choice == "3":
            system.update_employee()
        elif choice == "4":
            system.delete_employee()
        elif choice == "5":
            system.list_all_employees()
        elif choice == "6":
            system.generate_department_reports()
        elif choice == "7":
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")

# Start the system
if __name__ == "__main__":
    run()
