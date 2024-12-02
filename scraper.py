import requests
from bs4 import BeautifulSoup
from databases.DB import DB
import re
from pydantic import BaseModel
from typing import List

class AnswerAddJSON(BaseModel):
    content: str
    correct: bool

class SolutionAddJSON(BaseModel):
    content: str

class QuestionAddJSON(BaseModel):
    content: str
    difficulty: int
    answers: List[AnswerAddJSON]
    solutions: List[SolutionAddJSON]

db_instance = DB()

def add_question(question: QuestionAddJSON):
    answers = []
    for answer in question.answers: #turns all answer json into dict
        answers.append(answer.__dict__)
    solutions = []
    for solution in question.solutions: #turns all solution json into dict
        solutions.append(solution.__dict__)
    try:
        question_id = db_instance.add_question(question.content, difficulty=question.difficulty)
        for answer in question.answers:
            db_instance.add_answer(question_id, answer.content, answer.correct)

        for solution in question.solutions:
            db_instance.add_solution(question_id, solution.content)

        return {"success":True,
                "message":"placeholder"}
    except:
        return {"success":False,
                "error_code":"placeholder",
                "error_message":"Question failed to be added"}

def process_string(input_string):
    # If the string contains 'frac' or 'dfrac', disregard it
    if 'frac' in input_string or 'dfrac' in input_string:
        return None

    # Remove parentheses, brackets, and their content
    input_string = re.sub(r'[()\[\]{}]', '', input_string)

    # Remove content between < and > (i.e., tags or other content inside angle brackets)
    input_string = re.sub(r'<.*?>', '', input_string)

    # Remove specific words: 'qquad', 'text', 'math'
    input_string = re.sub(r'\b(qquad|text|math)\b', '', input_string)

    # Remove the tilde character (~)
    input_string = input_string.replace('~', '')

    # If the string starts with 'E', remove everything after a page break (if any)
    if input_string.startswith('E'):
        input_string = input_string.split('\n')[0]  # Keep only the part before any page break

    # Remove page breaks/newlines
    input_string = input_string.replace('\n', '').replace('\r', '')

    return input_string.strip()

def process_list_of_strings(strings):
    result_list = []
    for string in strings:
        processed_string = process_string(string)
        if processed_string:  # Only add to the result if it's not None or empty
            result_list.append(processed_string)
    return result_list
    
answers = """E
C
A
E
C
B
C
B
B
B
C
C
B
D
E
B
E
C
E
D
C
A
A
C
A""".split('\n')

year = 2020
test = "10A"
probs = 25
for i in range(probs):
    url = f'https://artofproblemsolving.com/wiki/index.php?title={year}_AMC_{test}_Problems/Problem_{i + 1}&action=edit'
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        exit()

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 3: Extract data from the parsed HTML
    # Example: Find all <h2> elements on the page
    contents = soup.find_all('textarea')

    # Process the extracted data
    if len(contents) == 1:
        for content in contents:
            print(content)
            question = content.text.split('==')[2]

            question = question.replace("<math>", "\(")
            question = question.replace("</math>", "\)")
            
            add_question(QuestionAddJSON(**{
    "content" : question,
    "difficulty" : i // 5 + 1,
    "answers" : [
                AnswerAddJSON(**{"content" : "A", "correct" : answers[i]=="A"}),
                AnswerAddJSON(**{"content" : "B", "correct" : answers[i]=="B"}),
                AnswerAddJSON(**{"content" : "C", "correct" : answers[i]=="C"}),
                AnswerAddJSON(**{"content" : "D", "correct" : answers[i]=="D"})
                ],
    "solutions" : []}))

            #db_instance.adaped(problem_text=question, correct_answer=answers[i], difficulty=(i % 5 + 1))
    else:
        print(f"{i} NIGHTMARE!!!!")
        break
    
        
        
    
    # You can extract other elements similarly using soup.find() or soup.select()
