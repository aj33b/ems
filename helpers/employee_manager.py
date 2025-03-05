from helpers.database import Database
import csv

class EmployeeManager:
    def __init__(self):
        self.db = Database()

    def add_employee(self,name, age, department, salary):
        conn = self.db.connect_database()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """INSERT INTO employees (name,age,department,salary) VALUES (%s,%s,%s,%s)"""
            cursor.execute(query,(name,age,department,salary))
            conn.commit()
            print(f"Employee added successfully!")
        except Exception as e:
            print(f"Error adding employee: {e}")
        finally:
            self.db.close()

    def view_employees(self):
        conn = self.db.connect_database()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM employees""")
            employees = cursor.fetchall()

            print("\nEmployee List:")
            for emp in employees:
                print(f"ID: {emp[0]}, Name: {emp[1]}, Age: {emp[2]}, Department: {emp[3]}, Salary: {emp[4]}")
            return employees
        except Exception as e:
            print(f"Error fetching employees: {e}")
        finally:
            self.db.close()

    def search_employee(self, name = None, department = None):
        conn = self.db.connect_database()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query= """SELECT * FROM employees WHERE name=%s OR department=%s"""
            cursor.execute(query,(name,department))
            employees = cursor.fetchall()

            print("\nSearch Results:")
            for emp in employees:
                print(f"ID: {emp[0]}, Name: {emp[1]}, Age: {emp[2]}, Department: {emp[3]}, Salary: {emp[4]}")
        except Exception as e:
            print(f"Error searching employee: {e}")
        finally:
            self.db.close()

    def update_employee(self, emp_id, name, age, department, salary):
        conn = self.db.connect_database()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """UPDATE employees SET name=%s, age=%s, department=%s, salary=%s WHERE id=%s"""
            cursor.execute(query,(name,age,department,salary,emp_id))
            conn.commit()
            print (f"Successfully updated employee details!")
        except Exception as e:
            print (f"Error updating employee: {e}")
        finally:
            self.db.close()

    def delete_employee(self, emp_id):
        conn = self.db.connect_database()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """DELETE FROM employees WHERE id=%s"""
            cursor.execute(query,(emp_id,))
            conn.commit()
            print (f"Employee details deleted successfully!")
        except Exception as e:
            print(f"Error deleted employee: {e}")
        finally:
            self.db.close()

    def calculate_salary_statistics(self):
        conn = self.db.connect_database()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """SELECT MIN(salary), MAX(salary), AVG(salary) FROM employees"""
            cursor.execute(query)
            stats = cursor.fetchone()
            print(f"Minimum Salary: Rs. {stats[0]}, Maximum Salary: Rs. {stats[1]}, Average Salary: Rs. {stats[2]}")
        except Exception as e:
            print(f"Error calculating salary statistics: {e}")
        finally:
            self.db.close()

    def export_to_csv(self):
        try:
            employees = self.view_employees()
            if employees is None:
                raise ValueError("Error while fetching employees.")
            with open("employees.csv","w",newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID","Name","Age","Department","Salary"])
                writer.writerows(employees)
            print(f"Data exported to employees.csv")
        except Exception as e:
            print(f"Error exporting data: {e}")