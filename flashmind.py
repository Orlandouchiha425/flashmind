"""Author:  Orlando Valadez Salas
Date written: 12/8/24
Assignment:   Final Project Progress report
Short Desc:   This will quiz students and allow them to insert "flash cards" """


import tkinter as tk
from tkinter import messagebox
import random
import time


class FlashMindApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlashMind - Study Flashcards")

        # Initialize flashcards list
        self.flashcards = []

        # Timer variables
        self.start_time = None
        self.time_left = 60  # Timer for 1 minute

        # Create the home screen
        self.create_home_screen()

    def create_home_screen(self):
        """Create the home screen with options for creating flashcards, taking quizzes, etc."""
        self.clear_screen()

        tk.Label(self.root, text="Welcome to FlashMind!",
                 font=("Arial", 24)).pack(pady=20)

        tk.Button(self.root, text="Create Flashcards",
                  command=self.create_flashcard_screen).pack(pady=10)
        tk.Button(self.root, text="Take Quiz",
                  command=self.quiz_screen).pack(pady=10)
        tk.Button(self.root, text="View Flashcards",
                  command=self.view_flashcards_screen).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def clear_screen(self):
        """Clear the screen before displaying a new screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_flashcard_screen(self):
        """Screen for creating new flashcards."""
        self.clear_screen()

        tk.Label(self.root, text="Create a New Flashcard",
                 font=("Arial", 18)).pack(pady=20)

        # Entry for card title
        tk.Label(self.root, text="Flashcard Title:").pack(pady=5)
        self.card_title = tk.Entry(self.root, width=50)
        self.card_title.pack(pady=5)

        # Entry for card notes
        tk.Label(self.root, text="Flashcard Notes:").pack(pady=5)
        self.card_notes = tk.Entry(self.root, width=50)
        self.card_notes.pack(pady=5)

        # Save button
        tk.Button(self.root, text="Save Flashcard",
                  command=self.save_flashcard).pack(pady=10)
        tk.Button(self.root, text="Back to Home",
                  command=self.create_home_screen).pack(pady=10)

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
                 font=("Arial", 18)).pack(pady=20)

        # Listbox to show flashcards
        self.flashcard_listbox = tk.Listbox(self.root, width=50, height=10)
        self.flashcard_listbox.pack(pady=10)

        # Add flashcards to the listbox
        for card in self.flashcards:
            self.flashcard_listbox.insert(tk.END, card["title"])

        # Back button
        tk.Button(self.root, text="Back to Home",
                  command=self.create_home_screen).pack(pady=10)

    def quiz_screen(self):
        """Quiz screen with random flashcards."""
        self.clear_screen()

        # Quiz title
        tk.Label(self.root, text="Quiz Time!",
                 font=("Arial", 18)).pack(pady=20)

        # Timer display
        self.timer_label = tk.Label(
            self.root, text=f"Time Left: {self.time_left}s", font=("Arial", 14))
        self.timer_label.pack(pady=10)

        # Select a random flashcard
        if self.flashcards:
            self.current_card = random.choice(self.flashcards)
            question = self.current_card["title"]
            self.correct_answer = self.current_card["notes"]

            tk.Label(self.root, text=f"Question: {question}", font=(
                "Arial", 14)).pack(pady=10)

            # Entry for user answer
            self.user_answer = tk.Entry(self.root, width=50)
            self.user_answer.pack(pady=5)

            # Button to submit the answer
            tk.Button(self.root, text="Submit Answer",
                      command=self.submit_answer).pack(pady=10)

            # Start the timer when the quiz starts
            self.start_timer()

            # Back button
            tk.Button(self.root, text="Back to Home",
                      command=self.create_home_screen).pack(pady=10)
        else:
            tk.Label(self.root, text="No flashcards available for the quiz.", font=(
                "Arial", 14)).pack(pady=20)
            tk.Button(self.root, text="Back to Home",
                      command=self.create_home_screen).pack(pady=10)

    def start_timer(self):
        """Start the timer for the quiz."""
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        """Update the timer display."""
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            remaining_time = max(self.time_left - elapsed_time, 0)

            # Update timer label
            self.timer_label.config(text=f"Time Left: {remaining_time}s")

            if remaining_time > 0:
                self.root.after(1000, self.update_timer)  # Update every second
            else:
                messagebox.showinfo("Time's Up!", "Your time is up!")
                self.submit_answer()

    def submit_answer(self):
        """Check if the user's answer is correct."""
        user_answer = self.user_answer.get().strip()

        if user_answer.lower() == self.correct_answer.lower():
            messagebox.showinfo("Correct!", "You got it right!")
        else:
            messagebox.showerror(
                "Incorrect", f"Wrong answer! The correct answer was: {self.correct_answer}")

        # Return to the quiz screen for next question or back to home
        self.quiz_screen()


# Running the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashMindApp(root)
    root.mainloop()
