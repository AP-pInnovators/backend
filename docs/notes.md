# Request Format

- Every request's first value will be "status" and will be either true or false AS A BOOLEAN VALUE (not a string)
- If the status of a request is false, the body will only have the next 2 following values (in order):
    - "error_code" : "some number that refers to a specific error"
    - "error_message" : "message describing the error"
- If the request returns true, the rest of the body will be normal depending on the content that is needed based on the endpoint that is called



# JSON Format for Entering New Questions and Answers

This is what the JSON sent to the adding questions endpoint should look like

```
{
    "content" : "question, answer 4 is correct",
    "difficulty" : integer from 1-10, might change later, 0 for undefined difficulty,
    "answers" : [
                {"content" : "answer 1", "correct" : false},
                {"content" : "answer 2", "correct" : false},
                {"content" : "answer 3", "correct" : false},
                {"content" : "answer 4", "correct" : true}
                ],
    "solutions" : [
                {"content" : "solution 1"},
                {"content" : "solution 2"},
                {"content" : "solution 3"},
                {"content" : "solution 4"}
                ]
}
```

### Example:

```
{
    "content" : "What is 1+3",
    "difficulty" : 1,
    "answers" : [
                {"content" : "1", "correct" : false},
                {"content" : "2", "correct" : false},
                {"content" : "3", "correct" : false},
                {"content" : "4", "correct" : true}
                ],
    "solutions" : [
                {"content" : "Add 1 to 3"},
                {"content" : "Add 3 to 1"}
                ]
}
```