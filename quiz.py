from questions import Question
import random

class Quiz:
    """
    Manages the quiz logic, including questions, scoring, and progress.
    """
    def __init__(self, questions: list[Question]):
        if not questions:
            raise ValueError("Cannot create a quiz with no questions.")
        self.questions = questions
        self.total_questions = len(self.questions)
        self.current_question_index = 0
        self.score = 0
        # Shuffle the questions for a different order each time
        random.shuffle(self.questions)

    def get_current_question(self) -> Question:
        """Returns the current question."""
        if not self.is_finished():
            return self.questions[self.current_question_index]
        return None

    def check_answer(self, user_answer: str) -> bool:
        """
        Checks the user's answer against the correct one.
        Updates the score if correct.
        """
        current_question = self.get_current_question()
        # Case-insensitive and strip whitespace for flexible checking
        is_correct = user_answer.strip().lower() == current_question.german_answer.strip().lower()
        if is_correct:
            self.score += 1
        return is_correct

    def next_question(self):
        """Moves to the next question."""
        if self.current_question_index < self.total_questions:
            self.current_question_index += 1

    def is_finished(self) -> bool:
        """Checks if the quiz has ended."""
        return self.current_question_index >= self.total_questions

    def get_score(self) -> tuple[int, int]:
        """Returns the current score and the total number of questions."""
        return self.score, self.total_questions
