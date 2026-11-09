import csv
from abc import ABC, abstractmethod


# 1. ABSTRACTION & ENCAPSULATION: Base Student Class
class Student(ABC):

    def __init__(self, name, math, english, science):
        self.name = name
        # Encapsulation: Storing data in a protected dictionary using a leading underscore
        self._scores = {"Math": math, "English": english, "Science": science}

    @property
    def final_score(self):
        """Getter method to securely calculate and return the average score."""
        return sum(self._scores.values()) / len(self._scores)

    # Abstraction: Forcing child classes to implement their own scholarship rules
    @abstractmethod
    def check_scholarship_eligibility(self):
        pass

    def get_grade(self):
        """Helper method to determine alphabetical grade."""
        score = self.final_score
        if score >= 80:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 40:
            return "C"
        return "F"


# 2. INHERITANCE, POLYMORPHISM & OVERRIDING: Regular Student
class RegularStudent(Student):

    def check_scholarship_eligibility(self):
        # Polymorphism / Overriding: Regular students need a stricter 85+ average
        return "Eligible" if self.final_score >= 80 else "Not Eligible"


# 2. INHERITANCE, POLYMORPHISM & OVERRIDING: Sports Student
class SportsStudent(Student):

    def check_scholarship_eligibility(self):
        # Polymorphism / Overriding: Sports students get a relaxed 70+ average threshold
        return "Eligible" if self.final_score >= 72 else "Not Eligible"


# 3. METHOD OVERLOADING & ANALYSIS
class PerformanceAnalyzer:

    # Overloading: Using *args (variable-length arguments) to dynamically accept any number of students
    def calculate_summary(self, *students):
        """Calculates highest, lowest, and class average using variable arguments."""
        if not students:
            return 0, 0, 0

        scores = [s.final_score for s in students]
        highest = max(scores)
        lowest = min(scores)
        average = sum(scores) / len(scores)

        return highest, lowest, average


# 4. EXECUTION & REPORT GENERATION
def main():
    students = []

    # Reading the CSV file using your exact field names: name, mat, eng, sci
    with open("students.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for index, row in enumerate(reader):
            # Converts string values from CSV directly into numbers
            m, e, s = int(row["MAT"]), int(row["ENG"]), int(row["SCI"])

            # Dynamically splits students into different OOP types for presentation purposes
            if index < 2:
                student = RegularStudent(row["NAME"], m, e, s)
            else:
                student = SportsStudent(row["NAME"], m, e, s)

            students.append(student)

    # Output student performance report
    print("\n--- STUDENT PERFORMANCE REPORT ---")
    print(f"{'Name':<15} {'Average':<10} {'Grade':<8} {'Scholarship':<12}")
    print("-" * 50)
    for s in students:
        print(
            f"{s.name:<15} {s.final_score:<10.2f} {s.get_grade():<8} {s.check_scholarship_eligibility():<12}"
        )

    # Class summary analysis using the analyzer tool
    analyzer = PerformanceAnalyzer()
    # Unpacking the array into individual arguments using the '*' operator
    hi, lo, avg = analyzer.calculate_summary(*students)

    print("\n--- CLASS SUMMARY STATS ---")
    print(f"Highest Class Average: {hi:.2f}")
    print(f"Lowest Class Average:  {lo:.2f}")
    print(f"Overall Class Average: {avg:.2f}")


if __name__ == "__main__":
    main()
