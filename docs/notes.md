# Request Format

- Every request's first value will be "status" and will be either true or false
- If the status of a request is false, the body will only have the next 2 following values (in order):
    - "error_code" : "some number that refers to a specific error"
    - "error_message" : "message describing the error"
- If the request returns true, the rest of the body will be normal depending on the content that is needed based on the endpoint that is called