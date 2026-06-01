def calculate_grade(marks):
    if marks >= 90:
        return "A", "Excellent! Keep it up! 🌟"
    elif marks >= 80:
        return "B", "Very Good! Keep it up! 👍"
    elif marks >= 70:
        return "C", "Good Job! 😊"
    elif marks >= 60:
        return "D", "You can do better! 💪"
    else:
        return "F", "Work harder and try again! 📚"

name = input("Enter student name: ")

while True:
    marks = int(input("Enter marks (0-100): "))

    if 0 <= marks <= 100:
        break
    else:
        print("Invalid marks! Please enter between 0 and 100.")

grade, message = calculate_grade(marks)

print("\n📊 RESULT")
print("Student Name:", name)
print("Marks:", marks)
print("Grade:", grade)
print("Message:", message)
