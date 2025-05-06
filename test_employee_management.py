# Importing unittest framework and mocking tools
import unittest
from unittest.mock import patch, mock_open
from io import StringIO  # For capturing print output



# Import classes and validation functions from the main program
from pdwd_pfs_a03_skeleton import (
    Employee,
    EmployeeManagementSystem,
    validate_employee_id,
    validate_name,
    validate_department,
    validate_salary,
    validate_contact
)



class TestEmployee(unittest.TestCase):


    def setUp(self):
        # Setup a sample Employee object for reuse in tests
        self.employee = Employee("E12345678", "John Doe", "HR", "5000", "john.doe@example.com")

    def test_employee_initialization(self):
        # Test correct assignment of all attributes
        self.assertEqual(self.employee.emp_id, "E12345678")
        self.assertEqual(self.employee.name, "John Doe")
        self.assertEqual(self.employee.department, "HR")
        self.assertEqual(self.employee.salary, 5000.0)
        self.assertEqual(self.employee.contact, "john.doe@example.com")

    def test_employee_str_output(self):
        # Test __str__ method contains expected fields
        output = str(self.employee)
        self.assertIn("John Doe", output)
        self.assertIn("HR", output)
        self.assertIn("$5000.00", output)


    def test_employee_to_dict(self):
        # Test dictionary representation for saving to CSV
        expected = {
            "ID": "E12345678",
            "Name": "John Doe",
            "Department": "HR",
            "Salary": "5000.00",
            "Contact": "john.doe@example.com"
        }
        self.assertEqual(self.employee.to_dict(), expected)



class TestEmployeeManagementSystem(unittest.TestCase):

    def setUp(self):
        # Create a fresh EMS object and reset the employee list
        self.ems = EmployeeManagementSystem()
        self.ems.employees = []


    def test_validations(self):
        # Test that all validation functions return True for valid inputs
        self.assertTrue(validate_employee_id("E12345678"))
        self.assertTrue(validate_name("Alice"))
        self.assertTrue(validate_department("Finance"))
        self.assertTrue(validate_salary("8000"))
        self.assertTrue(validate_contact("test@example.com"))


    def test_find_employee(self):
        # Add an employee and test if it can be found by ID
        emp = Employee("E10000001", "Jane", "IT", "7000", "jane@example.com")
        self.ems.employees.append(emp)
        found = self.ems.find_employee_by_id("E10000001")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Jane")


    @patch("builtins.input", side_effect=["E11111111", "Alice", "IT", "7000", "alice@example.com"])
    @patch("builtins.open", new_callable=mock_open)
    def test_add_employee(self, mock_file, mock_input):
        # Simulate user input and test if employee is added correctly
        self.ems.add_employee()
        self.assertEqual(len(self.ems.employees), 1)
        self.assertEqual(self.ems.employees[0].name, "Alice")

    @patch("builtins.input", side_effect=["E99999999"])
    def test_view_employee_not_found(self, mock_input):
        # Simulate input for a non-existent employee and capture output
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.ems.view_employee()
            self.assertIn("Employee not found", fake_out.getvalue())


    @patch("builtins.input", side_effect=[
        "E12345678", "Updated Name", "Admin", "9000", "updated@example.com", "yes"
    ])
    def test_update_employee(self, mock_input):
        # Add an employee, simulate update inputs and test updated values
        emp = Employee("E12345678", "Original", "HR", "8000", "original@example.com")
        self.ems.employees.append(emp)

        with patch("sys.stdout", new=StringIO()):  # Suppress output
            self.ems.update_employee()

        updated = self.ems.find_employee_by_id("E12345678")
        self.assertEqual(updated.name, "Updated Name")
        self.assertEqual(updated.department, "Admin")
        self.assertEqual(updated.salary, 9000.0)
        self.assertEqual(updated.contact, "updated@example.com")


    @patch("builtins.input", side_effect=["E12345678", "yes"])
    def test_delete_employee(self, mock_input):
        # Add an employee and simulate deletion confirmation
        emp = Employee("E12345678", "ToDelete", "Ops", "6000", "delete@example.com")
        self.ems.employees.append(emp)
        self.ems.delete_employee()
        self.assertEqual(len(self.ems.employees), 0)


    @patch("builtins.input", side_effect=["HR"])
    def test_department_wise_report(self, mock_input):
        # Add employees to different departments, simulate input, and verify report output
        emp1 = Employee("E10000001", "Alpha", "HR", "4000", "a@example.com")
        emp2 = Employee("E10000002", "Beta", "HR", "6000", "b@example.com")
        emp3 = Employee("E10000003", "Gamma", "IT", "5000", "c@example.com")
        self.ems.employees = [emp1, emp2, emp3]

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.ems.department_wise_report()
            output = fake_out.getvalue()
            self.assertIn("Alpha", output)
            self.assertIn("Beta", output)
            self.assertIn("Total Budgeted Salary for 'Hr': $10000.00", output)



if __name__ == "__main__":
    unittest.main()