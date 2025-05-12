import unittest
from unittest.mock import patch, mock_open, MagicMock
from io import StringIO

# Import relevant classes and validation functions from the main EMS system
from BitFutura_Employee_Management_System import (
    Employee,
    EmployeeManagementSystem,
    validate_employee_id,
    validate_name,
    validate_department,
    validate_salary,
    validate_contact
)

class TestEmployee(unittest.TestCase):
    """
    Unit tests for the Employee class.
    Tests initialization, string representation, and dictionary conversion.
    """

    def setUp(self):
        """Creates a sample employee object for repeated use in tests."""
        self.employee = Employee("E12345678", "John Doe", "HR", "5000", "john.doe@example.com")

    def test_employee_initialization(self):
        """Tests whether the Employee object is correctly initialized with expected values."""
        self.assertEqual(self.employee.emp_id, "E12345678")
        self.assertEqual(self.employee.name, "John Doe")
        self.assertEqual(self.employee.department, "HR")
        self.assertEqual(self.employee.salary, 5000.0)
        self.assertEqual(self.employee.contact, "john.doe@example.com")

    def test_employee_str_output(self):
        """Tests the string output (__str__) for formatting and expected fields."""
        output = str(self.employee)
        self.assertIn("John Doe", output)
        self.assertIn("HR", output)
        self.assertIn("$5000.00", output)

    def test_employee_to_dict(self):
        """Tests the dictionary conversion of an Employee object (used for saving to CSV)."""
        expected = {
            "ID": "E12345678",
            "Name": "John Doe",
            "Department": "HR",
            "Salary": "5000.00",
            "Contact": "john.doe@example.com"
        }
        self.assertEqual(self.employee.to_dict(), expected)

class TestEmployeeManagementSystem(unittest.TestCase):
    """
    Unit tests for EmployeeManagementSystem class.
    Covers add, update, delete, search, view, and report functions.
    """

    def setUp(self):
        """Initializes a fresh EMS instance with an empty employee list and a mocked email sender."""
        self.ems = EmployeeManagementSystem()
        self.ems.employees = []
        self.ems.email_sender = MagicMock()  # Prevents actual emails from being sent

    def test_validations(self):
        """Tests all validation helper functions with valid inputs."""
        self.assertTrue(validate_employee_id("E12345678"))
        self.assertTrue(validate_name("Alice"))
        self.assertTrue(validate_department("Finance"))
        self.assertTrue(validate_salary("8000"))
        self.assertTrue(validate_contact("test@example.com"))

    def test_find_employee(self):
        """Tests the ability to find an employee by ID after adding one."""
        emp = Employee("E10000001", "Jane", "IT", "7000", "jane@example.com")
        self.ems.employees.append(emp)
        found = self.ems.find_employee_by_id("E10000001")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Jane")

    @patch("builtins.input", side_effect=["E11111111", "Alice", "IT", "7000", "alice@example.com", "yes"])
    @patch("builtins.open", new_callable=mock_open)
    def test_add_employee(self, mock_file, mock_input):
        """
        Simulates adding an employee via mocked input.
        Verifies employee is added and confirmation email is triggered.
        """
        self.ems.add_employee()
        self.assertEqual(len(self.ems.employees), 1)
        self.assertEqual(self.ems.employees[0].name, "Alice")
        self.ems.email_sender.send_email.assert_called_once()

    @patch("builtins.input", side_effect=["E99999999"])
    def test_view_employee_not_found(self, mock_input):
        """
        Simulates a view attempt for a non-existent employee.
        Asserts correct 'not found' message is printed.
        """
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.ems.view_employee()
            self.assertIn("Employee not found", fake_out.getvalue())

    @patch("builtins.input", side_effect=[
        "E12345678", "yes",  # first confirmation
        "Updated Name", "Admin", "9000", "updated@example.com", "yes"  # new data + save confirmation
    ])
    def test_update_employee(self, mock_input):
        """
        Tests the update workflow including both confirmations.
        Verifies values are correctly updated in the employee record.
        """
        emp = Employee("E12345678", "Original", "HR", "8000", "original@example.com")
        self.ems.employees.append(emp)
        with patch("sys.stdout", new=StringIO()):
            self.ems.update_employee()

        updated = self.ems.find_employee_by_id("E12345678")
        self.assertEqual(updated.name, "Updated Name")
        self.assertEqual(updated.department, "Admin")
        self.assertEqual(updated.salary, 9000.0)
        self.assertEqual(updated.contact, "updated@example.com")

    @patch("builtins.input", side_effect=["E12345678", "yes", "yes"])
    def test_delete_employee(self, mock_input):
        """
        Tests the full deletion flow including both confirmations.
        Verifies employee is removed from the EMS list.
        """
        emp = Employee("E12345678", "ToDelete", "Ops", "6000", "delete@example.com")
        self.ems.employees.append(emp)
        with patch("sys.stdout", new=StringIO()):
            self.ems.delete_employee()
        self.assertEqual(len(self.ems.employees), 0)

    @patch("builtins.input", side_effect=["HR", "yes"])
    def test_department_wise_report(self, mock_input):
        """
        Tests the department-wise report generation.
        Verifies matching employees and total salary are printed.
        """
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

# Ensures test script can run directly from CLI or terminal
if __name__ == "__main__":
    unittest.main()
