import random


class Quiz:
    def __init__(self, questions, num_questions=None):
        """
        Initializes the quiz.
        :param questions: A list of Question objects.
        :param num_questions: The number of questions to include in the quiz.
                            If None or greater than available, all questions are used.
        """

        # Determine how many questions to sample
        num_to_sample = len(questions)
        if num_questions is not None and num_questions > 0 and num_questions < len(questions):
            num_to_sample = num_questions

        # Randomly sample the desired number of questions
        # This both shuffles and selects the right number.
        self.questions = random.sample(questions, num_to_sample)

        self.current_question_index = 0
        self.score = 0
        # The total number of questions is now the length of our sampled list
        self.total_questions = len(self.questions)

    def get_current_question(self):
        """Returns the current Question object."""
        if not self.is_finished():
            return self.questions[self.current_question_index]
        return None

    def check_answer(self, user_answer):
        """Checks the user's answer and updates the score."""
        question = self.get_current_question()
        if not question:
            return False

        # Case-insensitive and strip whitespace for more lenient checking
        is_correct = user_answer.strip().lower() == question.german_answer.strip().lower()

        if is_correct:
            self.score += 1

        return is_correct

    def next_question(self):
        """Advances to the next question."""
        if not self.is_finished():
            self.current_question_index += 1

    def is_finished(self):
        """Returns True if the quiz is over, False otherwise."""
        return self.current_question_index >= self.total_questions

    def get_score(self):
        """Returns the current score and total number of questions."""
        return self.score, self.total_questions

