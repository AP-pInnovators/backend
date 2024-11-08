Create a function in main.py that both prints out and logs errors to a file (right now everything is just printing)

After doing the above part, add logging to literally everything (probably make a general logging file and an error logging file seperately)

Make it so error messages are ambiguous based on whether they get username or password wrong

Make it so username has character limit, doesn't allow certain characters, basic stuff

Make it so email has to be a valid email (and add email verification later... much later lol)

Make it so password has to be certain length


Make error codes json file with corresponding messages, so that frontend can have it and import it so both backend and frontend can store error messages

Make JWT tokens last forever, and also once I add back timed JWT tokens make an endpoint to refresh your session