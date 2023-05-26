# Vaccine_Scheduler
**Team Members**: Patrick Xiao, Linh Nguyen, Jared Elliott

## Project Objective
This project can serve for two kinds of users: patients and caregivers.<br>
For patients: our patients can login our system, search for caregiver's avaliability,
and make or cancel reservation.<br>
For caregivers: our caregivers can upload their avalibility and new doeses of vaccines (if have), 
check and cancel reservation.<br>
Our database is hosted on Azure. You can access our database by VSCode connecting to Azure database.<br>

## Usage
Note that our project can only be run on Windows system with conda environment.
Enter the following commends into the Windows Git Bash terminal (preferred VSCode): <br>
- Step 1: Git clone our repoistory with `git clone git@github.com:PatrickShawn/vaccine_scheduler.git` <br>
- Step 1: Select your python python interpreter. For VS Code, press F1, type python to select "Python: Select Interpreter", and select the "base" environment. <br>
- Step 2: Create a virtual environment using `conda env create -f environment.yml` <br>
- Step 3: Change your current directory with `cd vaccine_scheduler/vaccine-scheduler-python-master/src/main`<br>
- Step 4: Insert raw data into database with `python Insertion.py` <br>
- Step 5: Set flask environment variable with  `export FLASK_APP=vaccine_scheduler` <br>
- Step 5: Run flask app with  `flask run` <br>
- Step 6: Copy the URL link `http://127.0.0.1:5000` to your favourite browser and begin your adventure! <br>

## Conda environment
Please follow the link to install conda in your Windows system. <br>
https://docs.anaconda.com/free/anaconda/install/windows/ <br>

## Azure Database
The database credentials are stored in the tcss545 environment variables. You can check them by the commend `conda env config vars list`. <br>
 <br>
To be specific: <br>
server name: `<Server>`.database.windows.net <br>
Database name: `<DBname>` <br>
Authentication Type: `SQL login` <br>
User name: `<UserID>` <br>
Password: `<Password>` <br>
After getting these values, please follow each steps in the prompt to complete configuration. <br>
 <br>
How to access our database on Azure: <br>
- Step 1: Install the mssql extension in VSCode. <br>
- Step 2: Connect to SQL Server (Azure) <br>
<br>
Here are two tutorials to walk through each step:<br>
https://learn.microsoft.com/en-us/sql/tools/visual-studio-code/mssql-extensions?view=sql-server-ver15#install-the-mssql-extension-in-vs-code <br>
https://learn.microsoft.com/en-us/sql/tools/visual-studio-code/sql-server-develop-use-vscode?view=sql-server-ver15 <br>

