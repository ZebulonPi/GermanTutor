from dataclasses import dataclass

@dataclass
class Question:
    """A data class to hold the structure of a single question."""
    english_sentence: str
    german_verb: str
    german_answer: str

def load_questions(filepath: str) -> list[Question]:
    """
    Loads questions from a text file.
    Each line in the file should be in the format:
    english_sentence;german_verb;german_answer
    """
    questions = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # Ignore empty lines or lines that are comments
                if line.strip() and not line.strip().startswith('#'):
                    parts = line.strip().split(';')
                    if len(parts) == 3:
                        questions.append(Question(
                            english_sentence=parts[0].strip(),
                            german_verb=parts[1].strip(),
                            german_answer=parts[2].strip()
                        ))
                    else:
                        print(f"Warning: Skipping malformed line: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        # Return a default question to prevent the app from crashing
        return [Question("File not found", "error", "Please create 'questions.txt'")]
    return questions
