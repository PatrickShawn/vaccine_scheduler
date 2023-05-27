# Vaccine_Scheduler
**Team Members**: Patrick Xiao, Linh Nguyen, Jared Elliott

## Project Objective
This project can serve for two kinds of users: patients and caregivers.<br>
For patients: our patients can login our system, search for caregiver's avaliability,
and make or cancel reservation.<br>
For caregivers: our caregivers can upload their avalibility and new doeses of vaccines (if have),
check and cancel reservation.<br>
Our database is hosted on Azure. You can access our database by VSCode connecting to Azure database.<br>
Note that our project can only be run on Windows system with conda environment. <br>
We recommend using VSCode as the IDE for running this project. <br>
<br>

## Setting up Anaconda Environment
First, set up your anaconda environment by the following steps: <br>
- Step 1: Download our project by clicking on the green button “Code” and select “Download ZIP” from the drop-down menu <br>
- Step 2: Install anaconda on your windows system if you haven't got it on your system.
- Step 3: Add anaconda path to windows environment variable.
- Step 4: Open your VSCode and install Python extension if you haven't installed it yet.
- Step 5: Select your python python interpreter in VSCode: press F1, type python to select "Python: Select Interpreter", and select the "(base)" environment. <br>

## Running Application
Then, open a new Windows Command Prompt terminal, and enter the following commands: <br>
- Step 1: Locate your current directory to application directory by `cd vaccine_scheduler/vaccine-scheduler-python-master/src/main`<br>
- Step 2: Import and create a virtual environment using `conda env create -f environment.yml` <br>
- Step 3: Switch to the created virtual environment using `conda activate tcss545` <br>
- Step 4: Insert raw data into database with `python Insertion.py` <br>
- Step 5: Set flask environment variable with  `set FLASK_APP=vaccine_scheduler` <br>
- Step 6: Run flask app with  `flask run` <br>
- Step 7: Copy the URL link `http://127.0.0.1:5000` to your favourite browser and begin your adventure! <br>

## Anaconda environment
Please follow the link to install anaconda in your Windows system. <br>
https://docs.anaconda.com/free/anaconda/install/windows/ <br>
Please follow the link to add anaconda path to your environment variable. <br>
https://www.geeksforgeeks.org/how-to-setup-anaconda-path-to-environment-variable/ <br>


## Connect to Azure Database
You can also connect to our Azure Database to directly query with it. <br>
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
- Step 2: Connect to SQL Server (Azure). <br>
<br>
Here are two tutorials to walk through each step:<br>
https://learn.microsoft.com/en-us/sql/tools/visual-studio-code/mssql-extensions?view=sql-server-ver15#install-the-mssql-extension-in-vs-code <br>
https://learn.microsoft.com/en-us/sql/tools/visual-studio-code/sql-server-develop-use-vscode?view=sql-server-ver15 <br>

