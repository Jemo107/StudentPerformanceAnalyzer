import csv
import os
from abc import ABC, abstractmethod


# TASK 4 & 5: BASE STUDENT CLASS (ABSTRACTION & ENCAPSULATION)
class AIUStudent(ABC):

    def __init__(self, student_id, first_name, last_name, math, english, science):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        # Encapsulation: Storing test data inside a protected attribute
        self._scores = {"Math": math, "English": english, "Science": science}

    @property
    def full_name(self):
        """Helper property to merge strings cleanly."""
        return f"{self.first_name} {self.last_name}"

    @property
    def final_score(self):
        """Calculates and returns the student's average test score."""
        return sum(self._scores.values()) / len(self._scores)

    def get_grade(self):
        """Helper to determine alphabetical letter grades."""
        score = self.final_score
        if score >= 80:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 40:
            return "C"
        return "F"

    # TASK 5: Shared method blueprint for Polymorphism demonstration
    @abstractmethod
    def get_status_details(self):
        """Returns student-specific classification details."""
        pass


# TASK 4 & 5: INHERITANCE AND METHOD OVERRIDING
class ScholarshipStudent(AIUStudent):

    def __init__(self, student_id, first_name, last_name, math, english, science, scholarship_amount=150000):
        # Using super() to invoke the parent class constructor correctly
        super().__init__(student_id, first_name, last_name, math, english, science)
        # Added task-required unique attribute
        self.scholarship_amount = scholarship_amount

    def is_eligible(self):
        """Returns true if the student's average is at least 85."""
        return self.final_score >= 85

    # TASK 4 & 5: Overriding the shared method for type-specific behavior
    def get_status_details(self):
        """Overridden method providing scholarship-specific behavior."""
        status = "Maintained" if self.is_eligible() else "Probation (Below 85)"
        return f"Scholarship Holder [{status}] - Grant: KES {self.scholarship_amount:,}"


# TASK 5: Regular student subclass to complete the Polymorphism demonstration
class RegularStudent(AIUStudent):

    def get_status_details(self):
        """Implements the shared method with behavior appropriate to a regular student."""
        return "Regular Tuition-Paying Student"


# TASK 3: PERFORMANCE ANALYZER AND COMPOSITION
class PerformanceAnalyzer:

    # Composition: Accepts and works directly with a collection of student objects
    def __init__(self, students):
        self.students = students

    def highest_average(self):
        """Returns the student object with the highest average."""
        if not self.students:
            return None
        # Uses standard Python max function looking directly at the object property
        return max(self.students, key=lambda s: s.final_score)

    def lowest_average(self):
        """Returns the student object with the lowest average."""
        if not self.students:
            return None
        return min(self.students, key=lambda s: s.final_score)

    def class_average(self):
        """Calculates the average performance of the entire class."""
        if not self.students:
            return 0
        total = sum(s.final_score for s in self.students)
        return total / len(self.students)


# Flexible CSV mapping helper to prevent column string format crashes
def get_val(row, *keywords):
    for key, value in row.items():
        clean_key = str(key).strip().lower()
        for kw in keywords:
            if kw.lower() in clean_key:
                return value
    raise KeyError(f"Could not find a column matching: {keywords}")


# EXECUTION FLOW
def main():
    student_collection = []
    csv_filename = "students.csv"

    if not os.path.exists(csv_filename):
        print(f"Error: The file '{csv_filename}' was not found.")
        return

    try:
        with open(csv_filename, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                try:
                    s_id = get_val(row, "id", "student")
                    f_name = get_val(row, "fname", "first")
                    l_name = get_val(row, "lname", "last")
                    m = int(get_val(row, "mat"))
                    e = int(get_val(row, "eng"))
                    s = int(get_val(row, "sci"))
                    prog = get_val(row, "prog", "course")
                except (KeyError, ValueError) as err:
                    print(f"Skipping a bad row: {err}")
                    continue

                # Dynamically separating student types using the 'Programme' column
                if "MDA" in str(prog).upper():
                    # Instantiate scholarship students with customized constructor parameter
                    student = ScholarshipStudent(s_id, f_name, l_name, m, e, s, scholarship_amount=120000)
                else:
                    student = RegularStudent(s_id, f_name, l_name, m, e, s)

                student_collection.append(student)

    except Exception as error:
        print(f"Critical execution error: {error}")
        return

    if not student_collection:
        print("No valid data records loaded.")
        return

    # TASK 5 POLYMORPHISM DEMONSTRATION
    # Storing different student objects in one collection and calling the shared method in a loop
    print("\n" + "=" * 35 + " TASK 5: POLYMORPHISM LOOP " + "=" * 35)
    for s in student_collection:
        print(f"Student: {s.full_name:<18} | Avg: {s.final_score:<6.2f} | Info: {s.get_status_details()}")
    print("=" * 97)

    # TASK 3 PERFORMANCE ANALYZER DEMONSTRATION
    analyzer = PerformanceAnalyzer(student_collection)

    top_student = analyzer.highest_average()
    worst_student = analyzer.lowest_average()
    overall_avg = analyzer.class_average()

    print("\n" + "=" * 15 + " TASK 3: PERFORMANCE ANALYZER SUMMARY " + "=" * 15)
    if top_student:
        print(f"Highest Average Student: {top_student.full_name} ({top_student.final_score:.2f}%)")
    if worst_student:
        print(f"Lowest Average Student:  {worst_student.full_name} ({worst_student.final_score:.2f}%)")
    print(f"Overall Class Average:   {overall_avg:.2f}%")
    print("=" * 70)


if __name__ == "__main__":
    main()
