class Employee():
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def increaseSalary(self, increasePercentage):
        self.salary = self.salary * (1+increasePercentage)
        print(self.salary)

John = Employee("John", 5000)
John.increaseSalary(.1)
