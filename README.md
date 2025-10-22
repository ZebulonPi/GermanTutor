🇩🇩🇪 German Verb Conjugation Practice App

This is a simple web application built with Streamlit to help you practice conjugating German verbs in the present tense.

The app presents you with an English sentence (e.g., "I am drinking") and the base German verb (e.g., "trinken"). You must then type the full, correctly conjugated German sentence (e.g., "ich trinke"). The app provides instant feedback and tracks your score, allowing you to test your knowledge in a quiz format.

Features

Interactive Quiz: Practice with randomly shuffled questions.

Instant Feedback: See if your answer is correct right away.

Score Tracking: Your final score is displayed at the end of the quiz.

Extensible Content: Easily add new verbs and sentences by editing a simple text file.

Cheat Sheet: A handy popover shows German pronouns and their corresponding present tense verb endings.

🚀 How to Run This Application

1. Prerequisites

You must have Python 3 installed on your system.

2. Installation

Clone or Download the Project:
Ensure you have all the project files in the same directory:

german_conjugation_app.py

quiz.py

questions.py

questions.txt

german_pronouns.csv

Install Required Libraries:
This project requires streamlit and pandas. You can install them using pip:

pip install streamlit pandas



3. Run the App

Open your terminal or command prompt.

Navigate to the directory where you saved the project files.

Run the following command:

streamlit run german_conjugation_app.py



Your default web browser will automatically open with the running application.

📁 Project Structure

german_conjugation_app.py: The main Streamlit application file. It handles the UI, session state, and overall app flow.

quiz.py: A Python class that manages the quiz logic (tracking score, shuffling questions, checking answers).

questions.py: Contains the Question class and the logic for loading questions from questions.txt.

questions.txt: A plain text file containing all the practice sentences. This is the file you edit to add more content.

german_pronouns.csv: A CSV file containing the data for the "Cheat Sheet" popover.

README.md: This file.

✍️ How to Add More Questions

You can easily add your own verbs and sentences to the quiz.

Open the questions.txt file in any text editor.

Follow the simple format:
English Sentence;German Verb;Full German Answer

Example:

# --- Verb: schwimmen (to swim) ---
I am swimming;schwimmen;ich schwimme
you are swimming (informal);schwimmen;du schwimmst
he is swimming;schwimmen;er schwimmt



Lines starting with # are comments and will be ignored.

Ensure each question part is separated by a semicolon (;).

Save the file, and the new questions will be automatically loaded the next time you start or reset the app.