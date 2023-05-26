# Vaccine_Scheduler
**Team Members**: Patrick Xiao, Linh Nguyen, Jared Elliott

## Project Objective
This project can serve for two kinds of users: patients and caregivers.
For patients: our patients can login our system, search for caregiver's avaliability,<br>
and make or cancel reservation.
For caregivers: our caregivers can upload their avalibility and new doeses of vaccines (if have), <br>
check and cancel reservation.

## Usage
Note that our project can only be run on Windows system with conda environment.
Enter the following commends into the Windows Git Bash terminal (preferred VS Code): <br>
- Step 1: Git clone our repoistory with `git clone git@github.com:PatrickShawn/vaccine_scheduler.git` <br>
- Step 1: Select your python python interpreter. For VS Code, press F1, type python to select "Python: Select Interpreter", and select the "base" environment. <br>
- Step 2: Create a virtual environment using `conda env create -f environment.yml` <br>
- Step 3: Change your current directory with `cd vaccine_scheduler/vaccine-scheduler-python-master/src/main`<br>
- Step 4: Insert raw data into database with `python Insertion.py` <br>
- Step 5: Set flask environment variable with  `export FLASK_APP=vaccine_scheduler` <br>
- Step 5: Run flask app with  `flask run` <br>
- Step 6: Copy the URL link `http://127.0.0.1:5000` to your favourite browser and begin your adventure! <br>