import pickle
import textwrap

with open('tests/api/resources/constants', 'rb') as file:
    constants_file = pickle.load(file)

    TEST_COLLECTION_NAME = "test_collection"
    TEST_TEXT_A = "Lorem ipsum"
    TEST_VECTOR_A = constants_file[0]
    TEST_TEXT_B = "dolor sit amet"
    TEST_VECTOR_B = constants_file[1]
    TEST_SOURCE_TEXT = constants_file[2]
    TEST_SOURCE_FILENAME_A = constants_file[3]
    TEST_SOURCE_FILENAME_B = "Enter the Wu-Tang (36 Chambers).docx"
    TEST_EMBEDDING_RESPONSE = constants_file[4]

TEST_QUESTION = "What is the meaning of life?"
TEST_CONTEXT = "The meaning of life is 42."
TEST_MESSAGES = [
    {"is_answer": False, "content": "test-question-1?", "context": "context-1."},
    {"is_answer": True, "content": "test-answer-1."},
]
TEST_INSTRUCTION = "This is a test instruction."
TEST_QUESTION_FORMAT = r"The question is {question} and the context is {context}"
TEST_ANSWER_FORMAT = r"The answer is {answer}"
TEST_PROMPT = textwrap.dedent(
    """
    This is a test instruction.
    
    The question is test-question-1? and the context is context-1.
    The answer is test-answer-1.
    The question is What is the meaning of life? and the context is The meaning of life is 42.
    The answer is 
    """
)
TEST_FILE_PATH = "tests/api/resources/sources"
