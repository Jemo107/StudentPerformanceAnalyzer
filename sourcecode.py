import csv
import os
from abc import ABC, abstractmethod


# 1. ABSTRACTION & ENCAPSULATION: Base Student Class
class Student(ABC):

    def __init__(self, student_id, first_name, last_name, math, english, science):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        # Encapsulation: Restricting direct access to raw scores
        self._scores = {"Math": math, "English": english, "Science": science}

    @property
    def full_name(self):
        """Helper property to merge first and last name cleanly."""
        return f"{self.first_name} {self.last_name}"

    @property
    def final_score(self):
        """Getter method to securely compute and return the average test score."""
        return sum(self._scores.values()) / len(self._scores)

    # Abstraction: Forcing child classes to define unique scholarship guidelines
    @abstractmethod
    def check_scholarship_eligibility(self):
        pass

    def get_grade(self):
        """Helper method to determine alphabetical letter grades."""
        score = self.final_score
        if score >= 80:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 40:
            return "C"
        return "F"


# 2. INHERITANCE, POLYMORPHISM & OVERRIDING: Regular Student (MDS Program)
class RegularStudent(Student):

    def check_scholarship_eligibility(self):
        return "Eligible" if self.final_score >= 85 else "Not Eligible"


# 2. INHERITANCE, POLYMORPHISM & OVERRIDING: Sports Student (MDA Program)
class SportsStudent(Student):

    def check_scholarship_eligibility(self):
        return "Eligible" if self.final_score >= 70 else "Not Eligible"


# 3. METHOD OVERLOADING & ANALYSIS
class PerformanceAnalyzer:

    def calculate_summary(self, *students):
        if not students:
            return 0, 0, 0
        scores = [s.final_score for s in students]
        return max(scores), min(scores), sum(scores) / len(scores)


# Helper function to find CSV columns flexibly (handles typos, spaces, or case issues)
def get_val(row, *keywords):
    """Searches a CSV row dictionary for keys matching any of the keywords loosely."""
    for key, value in row.items():
        # Strip spaces and convert to lowercase for comparison
        clean_key = str(key).strip().lower()
        for kw in keywords:
            if kw.lower() in clean_key:
                return value
    raise KeyError(f"Could not find a column matching: {keywords[0]}")


# 4. EXECUTION & REPORT GENERATION WITH ERROR HANDLING
def main():
    students = []
    csv_filename = "students.csv"

    if not os.path.exists(csv_filename):
        print(f"Error: The file '{csv_filename}' was not found.")
        return

    try:
        with open(csv_filename, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Dynamically fetches columns matching common variations
                    s_id = get_val(row, "id", "student")
                    f_name = get_val(row, "fname", "first")
                    l_name = get_val(row, "lname", "last")
                    prog = get_val(row, "prog", "course")

                    m = int(get_val(row, "mat"))
                    e = int(get_val(row, "eng"))
                    s = int(get_val(row, "sci"))
                except (KeyError, ValueError) as e:
                    print(f"Skipping a row due to data issue: {e}")
                    continue

                # Splitting student subtypes based on their 'Programme' column
                if "MDA" in str(prog).upper():
                    student = SportsStudent(s_id, f_name, l_name, m, e, s)
                else:
                    student = RegularStudent(s_id, f_name, l_name, m, e, s)

                students.append(student)

    except Exception as error:
        print(f"An unexpected error occurred: {error}")
        return

    if not students:
        print("No valid student records found to evaluate. Check your CSV headers.")
        return

    # Output individual performance records report
    print("\n--- STUDENT PERFORMANCE REPORT ---")
    print(f"{'ID':<8} {'Full Name':<18} {'Average':<10} {'Grade':<8} {'Scholarship':<12}")
    print("-" * 60)
    for s in students:
        print(
            f"{s.student_id:<8} {s.full_name:<18} {s.final_score:<10.2f} {s.get_grade():<8} {s.check_scholarship_eligibility():<12}")

    # Class summary analysis block execution
    analyzer = PerformanceAnalyzer()
    hi, lo, avg = analyzer.calculate_summary(*students)

    print("\n--- CLASS SUMMARY STATS ---")
    print(f"Highest Class Average: {hi:.2f}")
    print(f"Lowest Class Average:  {lo:.2f}")
    print(f"Overall Class Average: {avg:.2f}")


if __name__ == "__main__":
    main()
