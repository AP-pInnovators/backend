import requests
from bs4 import BeautifulSoup
from DB import DB

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
