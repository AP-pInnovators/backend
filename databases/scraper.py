import requests
from bs4 import BeautifulSoup
from DB import DB
import re

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
    
answers = """A
D
D
A
B
A
B
B
D
D
B
C
E
B
D
D
C
B
C
D
E
E
C
B
A""".split('\n')

db_instance = DB()

year = 2022
test = "10B"
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
            
            db_instance.add_scraped(problem_text=question, correct_answer=answers[i], difficulty=(i % 5 + 1))
    else:
        print(f"{i} NIGHTMARE!!!!")
        break
    
        
        
    
    # You can extract other elements similarly using soup.find() or soup.select()
