"""This program emulates a simple expense tracking program. It employs various functions
to add expenses to a list, save those expenses, and perform a certain number of 
operations on those expenses (total cost, matching of categories, etc.)

Task: Your task is to complete the implementation of the code and make sure that matches
the requirements set in the assignment's prompt.
First, you will have to make your code identifiable by setting the following information.

******************************************************
Name: Claude Kwizera
Andrew ID: ckwizera
Semester: Summer 2023
Course: Introduction to Python
Last modified: Fri June 23 12:122 Am 2023
******************************************************

"""

from typing import Tuple

## Declare a global variable to contain all the expenses processed in the program
expenses = []


class FileReadError(FileNotFoundError):
    """Exception class for errors that occur while reading a file."""
    pass

class FileWriteError(IOError):
    """Exception class for errors that occur while writing to a file."""
    pass

class BadNumberException(ValueError):
    """Exception class for invalid number inputs."""
    pass

class ValidateCategory(ValueError):
    """Exception class for category character count."""
    pass

class UtilClass:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        try:
            with open(self.file_path, 'r') as file:
                data = file.read()
            return data
        except IOError:
            raise FileReadError("Error reading data from the file.")

    def write_data(self, data):
        try:
            with open(self.file_path, 'w') as file:
                file.write(data)
        except IOError:
            raise FileWriteError("Error writing data to the file.")

    def validate_amount(self, amount) -> float:
        try:
            amount = float(amount)
            if amount < 0:
                raise BadNumberException("Invalid amount. Amount should be a positive number.")
            return amount
        except ValueError:
            raise BadNumberException("Invalid amount. Amount should be a valid number.")

    def validate_category(self, category):
        min_chars = 3 
        if not isinstance(category, str):
            raise ValidateCategory("Invalid category. Category should be a string.")
        if len(category) < min_chars:
            raise ValidateCategory(f"Invalid category. Category should have at least  {min_chars} characters.")


class ExpenseTracker:
    def __init__(self, file_path):
        self.file_path = file_path
        self.util = UtilClass(file_path)
        
    def add_expense(self,category: str, amount: float):
         global expenses
         try:
            self.util.validate_category(category)
            validated_amount = self.util.validate_amount(amount)
            expenses.append((category, validated_amount))
         except (ValidateCategory, BadNumberException) as e:
            raise ValueError(str(e))
    def dump_expenses(self):
      global expenses
      data = '\n'.join([f"{category},{amount}" for category, amount in expenses])
      self.util.write_data(data)
    def read_expenses(self):
        global expenses
        saved_expenses = []

        data = self.util.read_data()
        for line in data.split('\n'):
            line = line.strip()
            if line:
                category, amount = line.split(',')
                amount = float(amount)
                formatted_amount = "{:.2f}".format(amount)
                saved_expenses.append((category, formatted_amount))
        expenses += saved_expenses
  
    def get_expenses_by_category(self,category):
      global expenses
      matching_expenses = []
      for expense in expenses:
        expense_category, _ = expense
        if expense_category.casefold() == category.casefold():
            matching_expenses.append(expense)

      return matching_expenses
    def calculate_total_expenses(self): 
      global expenses
      total_amount = 0.0
      for expense in expenses:
         _, amount = expense
         total_amount += float(amount)

      return total_amount
    def get_menu_action(self) -> int:
           while True:
                  print('Menu:')
                  print('1. Add an expense')
                  print('2. View expenses by category')
                  print('3. Calculate total expenses')
                  print('4. Exit')

                  try:
                        choice = int(input("Enter your selection: "))
                        if choice in range(1, 5):
                           return choice
                        else:
                           print("Invalid input. Please enter a number from 1 to 4.")
                  except ValueError:
                        print("Invalid input. Please enter a number.")
    def print_expense(self,expense: Tuple[str, float]) -> str:
      category, amount = expense
      formatted_category = f"{category:<10}"
      formatted_amount = "${:<10}".format(amount)


      return f"|{formatted_category}|{formatted_amount}|"   

if __name__ == "__main__":
    file_path = "expenses.txt"
    tracker = ExpenseTracker(file_path)

    while True:
           command = tracker.get_menu_action()

           if command == 1:
                  try:
                     category = input("Enter the category: ")
                     amount = input("Enter the amount: ")
                     amount = tracker.util.validate_amount(amount)
                     tracker.add_expense(category, amount)
                     print("Expense added successfully.")
                  except (ValueError, BadNumberException) as e:
                     print(f"Invalid input: {str(e)}")
                  except (FileWriteError, FileReadError) as e:
                     print(f"Error accessing the file: {str(e)}")
           elif command == 2:
                  tracker.read_expenses()
                  category = input("Enter the category: ")
                  choosenExpenses = tracker.get_expenses_by_category(category)
                  if not choosenExpenses:
                     print("No expenses found for the given category.")
                  else:
                     print('|Category  |Amount    |')
                     print('***********************')
                     for expense in choosenExpenses:
                        print(tracker.print_expense(expense))
           elif command == 3:
                  total_expenses = tracker.calculate_total_expenses()
                  print(f"Total expenses: ${total_expenses:.2f}")

           elif command == 4:
               print("Exiting the Expense Tracker Application...")
               tracker.dump_expenses()
               break

           else:
            raise ValueError('Invalid command entered')

