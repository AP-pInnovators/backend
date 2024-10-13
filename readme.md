# Running the API server
Follow all the steps below when initially setting up the server to run on your machine. Once you did this once, you shouldn't need to redo it and can just paste the run command, but if anything breaks, use the process below to debug

The assumption here is that you're using VSCode and have Python installed properly with the Python VSCode extension (all on Windows, should be similar for Mac but might be different in some ways)

### Creating the venv
1. Close out of all VSCode terminals completely
2. Open the Command Palette in VSCode by pressing Ctrl + Shift + P
3. Type "interpreter" and find the option "Python: Select Interpreter"
4. Press "Create Virtual Environment..."
5. Press "Venv"
6. Select whatever Python interpreter path appears (should only be one if you installed Python correctly, but if there's more, then select the latest, ideally 3.11+; if there's none, try installing Python again)
7. Wait for the venv to finish being created, and then <strong>restart VSCode</strong> (important)
8. Open the Command Palette again and type "interpreter", selecting the option "Python: Select Interpreter" again
9. Select the option that says "Recommended" on the right (should be the path with "venv" in it)
10. Open the terminal and start a Python shell by typing ```python``` (if that doesn't work, try ```python3``` or ```py```)
11. Enter ```import sys```
12. Enter ```sys.prefix``` (after looking below exit with ```exit()```)

If the very end of the printed path says ".venv", then it worked

If not, make sure the venv is the selected interpreter, and that you restarted VSCode after selecting the interpreter

<strong>Now, any terminal you open in the project directory should be running the venv that is inside your project folder</strong>

### Downloading dependencies to the venv
In your VSCode terminal, run the following command (replace ```pip``` with ```pip3``` if it doesn't work):
```
pip install -r requirements.txt
```
Run this too, uvicorn doesn't work unless I install this for whatever reason
```
pip install -U email-validator
```

### Database Setup
1. When you have the project open in VSCode, make sure you have all the dependencies installed from above
2. Check your terminal to make sure you are CD'd into the projects root directory (make sure you are not in any folder such as testing, docs, databases, etc)
3. Once you have verified everything above, use the explorer to databases > database_setup > UserDB_setup.py and open the file in your editor
4. Run the file using the run button and the database should be set up correctly (if it doesn't work make sure you are running the file in the root project directory, hence step 2, or check dependencies/venv)


### Running App
Just run
```
uvicorn main:app --reload
```
in your terminal (or actually you could run the file normally, I made it work)

To stop the app, just press Ctrl + C while terminal is selected


### Running Jupyter Tester
Run
```
pip install requests
```
in your terminal to allow the tester to make requests to your app

When running the Jupyter file for the first time:
- If asked to select an interpreter, use the same venv from before
- If then asked to allow the installation of "ipykernel", say yes