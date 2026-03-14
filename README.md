Automatic Attendance Recognition System for GDPT Chanh Hoa

### Running the backend
- Go into the `backend` folder
- Create a python environment with `python3 -m venv .venv`
- Type `source .venv/bin/activate` to activate environment
- Type `pip install -r requirements.txt` in command prompt(this will install required packages for project)
- Run `python app.py`

### Running the front end
- Ensure you have node installed
- For developer mode, run `npm run dev`

# Todo
- Test the face recognition page to make sure it's working and adding sessions/attendance to the database properly.
- Allow the view attendance page to display all sessions and their attendance for a given date. Currently it only displays one subject even if multiple sessions are started within a day.
- Add an upload section for the photo capture when registering as a new member.
- Low priority: Allow attendance search by buddha name.
