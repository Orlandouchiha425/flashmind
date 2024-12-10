"""Author:  Orlando Valadez Salas
Date written: 12/8/24
Assignment:   Final Project Progress report
Short Desc:   This will quiz students and allow them to insert "flash cards" """

import tkinter as tk
from tkinter import messagebox
import random


class FlashMindApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlashMind - Study Flashcards")

        # Set app background color
        # self.root.configure(bg="gainsboro")

        # Initialize flashcards list with hardcoded examples
        self.flashcards = [
            {"title": "What is the total of print(1+1)?", "notes": "2"},
            {"title": "What is the result of  var1 = 1\nvar2 = 2\nvar3 = \"3\"\n\nprint(var1 + var2 + var3)",
             "notes": "Error"},
            {"title": "is this a test?", "notes": "yes"},
            {"title": "salary = 8000\n\n\ndef printSalary():\n    salary = 12000\n    print(\"Salary:\", salary)\n\n\nprintSalary()\nprint(\"Salary:\", salary)",
             "notes": "Salary: 12000\nSalary: 8000"}
        ]

        # Quiz variables
        self.quiz_questions = []
        self.current_index = 0
        self.correct_answers = 0

        # Create the home screen
        self.create_home_screen()

    def create_home_screen(self):
        """Create the home screen with options for creating flashcards, taking quizzes, etc."""
        self.clear_screen()

        tk.Label(self.root, text="Welcome to FlashMind!",
                 font=("Arial", 24), bg="#f0f8ff").pack(pady=20)

        tk.Button(self.root, text="Create Flashcards", bg='blue', fg='black',
                  font=("Arial", 12), command=self.create_flashcard_screen).pack(pady=10)

        tk.Button(self.root, text="Take Quiz", bg='blue', fg='black',
                  font=("Arial", 12), command=self.quiz_screen).pack(pady=10)

        tk.Button(self.root, text="View Flashcards", bg='blue', fg='black',
                  font=("Arial", 12), command=self.view_flashcards_screen).pack(pady=10)

        tk.Button(self.root, text="Exit", bg='blue', fg='black',
                  font=("Arial", 12), command=self.root.quit).pack(pady=10)

    def clear_screen(self):
        """Clear the screen before displaying a new screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_flashcard_screen(self):
        """Screen for creating new flashcards."""
        self.clear_screen()

        tk.Label(self.root, text="Create a New Flashcard",
                 font=("Arial", 18), bg="#f0f8ff").pack(pady=20)

        # Entry for card title
        tk.Label(self.root, text="Flashcard Title:",
                 bg="#f0f8ff", font=("Arial", 12)).pack(pady=5)
        self.card_title = tk.Entry(self.root, width=50)
        self.card_title.pack(pady=5)

        # Entry for card notes
        tk.Label(self.root, text="Flashcard Notes:",
                 bg="#f0f8ff", font=("Arial", 12)).pack(pady=5)
        self.card_notes = tk.Entry(self.root, width=50)
        self.card_notes.pack(pady=5)

        # Save button
        save_button = tk.Button(self.root, text="Save Flashcard", bg='blue', fg='black',
                                font=("Arial", 12), command=self.save_flashcard)
        save_button.pack(pady=10)

        # Bind Enter key to Save Flashcard action
        self.root.bind('<Return>', lambda event: self.save_flashcard())

        tk.Button(self.root, text="Back to Home", bg='blue', fg='black',
                  font=("Arial", 12), command=self.create_home_screen).pack(pady=10)

    def save_flashcard(self):
        """Save the flashcard details."""
        title = self.card_title.get()
        notes = self.card_notes.get()

        if title and notes:
            # Append to flashcards list
            self.flashcards.append({"title": title, "notes": notes})
            messagebox.showinfo("Flashcard Saved",
                                f"Flashcard '{title}' created successfully!")

            # Clear entry fields
            self.card_title.delete(0, tk.END)
            self.card_notes.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please fill in both fields!")

    def view_flashcards_screen(self):
        """Screen to view all created flashcards."""
        self.clear_screen()

        tk.Label(self.root, text="Your Flashcards",
                 font=("Arial", 18), bg="#f0f8ff").pack(pady=20)

        # Listbox to show flashcards
        self.flashcard_listbox = tk.Listbox(self.root, width=50, height=10)
        self.flashcard_listbox.pack(pady=10)

        # Add flashcards to the listbox
        for card in self.flashcards:
            self.flashcard_listbox.insert(tk.END, card["title"])

        # Back button
        tk.Button(self.root, text="Back to Home", bg='blue', fg='black',
                  font=("Arial", 12), command=self.create_home_screen).pack(pady=10)

    def quiz_screen(self):
        """Start the quiz with random flashcards."""
        self.clear_screen()

        if self.flashcards:
            self.quiz_questions = random.sample(
                self.flashcards, len(self.flashcards))
            self.current_index = 0
            self.correct_answers = 0
            self.display_next_question()
        else:
            tk.Label(self.root, text="No flashcards available for the quiz.", font=(
                "Arial", 14), bg="#f0f8ff").pack(pady=20)
            tk.Button(self.root, text="Back to Home", bg='blue', fg='black',
                      font=("Arial", 12), command=self.create_home_screen).pack(pady=10)

    def display_next_question(self):
        """Display the next question in the quiz."""
        if self.current_index < len(self.quiz_questions):
            question = self.quiz_questions[self.current_index]["title"]
            self.correct_answer = self.quiz_questions[self.current_index]["notes"]

            self.clear_screen()

            tk.Label(self.root, text=f"Question {self.current_index + 1}: {question}",
                     font=("Arial", 14), bg="#f0f8ff").pack(pady=20)

            self.user_answer = tk.Entry(self.root, width=50)
            self.user_answer.pack(pady=5)

            submit_button = tk.Button(self.root, text="Submit Answer", bg='blue', fg='black',
                                      font=("Arial", 12), command=self.submit_answer)
            submit_button.pack(pady=10)

            # Bind Enter key to Submit Answer action
            self.root.bind('<Return>', lambda event: self.submit_answer())
        else:
            self.show_score()

    def submit_answer(self):
        """Submit the user's answer for the current question."""
        user_answer = self.user_answer.get().strip()

        if user_answer.lower() == self.correct_answer.lower():
            self.correct_answers += 1

        self.current_index += 1
        self.display_next_question()

    def show_score(self):
        """Display the final score after the quiz ends."""
        self.clear_screen()

        total_questions = len(self.quiz_questions)
        score_percentage = (self.correct_answers / total_questions) * 100

        tk.Label(self.root, text=f"Quiz Complete!", font=(
            "Arial", 18), bg="#f0f8ff").pack(pady=20)
        tk.Label(self.root, text=f"Your Score: {self.correct_answers}/{total_questions} ({score_percentage:.2f}%)",
                 font=("Arial", 14), bg="#f0f8ff").pack(pady=10)

        tk.Button(self.root, text="Back to Home", bg='blue', fg='black',
                  font=("Arial", 12), command=self.create_home_screen).pack(pady=10)


# Running the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashMindApp(root)
    root.mainloop()
