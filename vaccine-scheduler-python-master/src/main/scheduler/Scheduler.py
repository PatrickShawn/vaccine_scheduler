from .model.Vaccine import Vaccine
from .model.Caregiver import Caregiver
from .model.Patient import Patient
from .util.Util import Util
from .db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    # create_patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create patient.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the patient
    patient = Patient(username, salt=salt, hash=hash)

    # save to patient information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create patient.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create patient.")
        print(e)
        return
    print("Created patient", username)


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create caregiver.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create caregiver.")
        print(e)
        return
    print("Created caregiver", username)


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_patient is not None or current_patient is not None:
        print("Patient already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    """
    search_caregiver_schedule <date>
    Check caregiver availability on a given date along with current vaccines doses.
    Part 2 Finished.
    """
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first!")
        return
    if len(tokens) != 2:
        print("Invalid args. Please try again")
        return
    date = tokens[1]
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    # Check if input date is valid
    try:
        d = datetime.datetime(year, month, day)
    except ValueError as e:
        print("Invalid date:", e)
        print("Please try again!")
        return
    # Check available caregivers
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)
    check_caregiver = "SELECT Username FROM Availabilities WHERE Time = %s ORDER BY Username ASC"
    try:
        cursor.execute(check_caregiver, d)
        results_caregivers = cursor.fetchall()
        if len(results_caregivers) == 0:
            print("No avaliable caregiver for this date")
        else:
            print("Selected date: {}".format(str(d)[:10]))
            print("Your select date have the following available caregivers:")
            for row in results_caregivers:
                print(row['Username'])
    except pymssql.Error as E:
        print("Error occurred when getting Caregivers")
        print("Please try again!")
        print("Db-Error:", E)
        quit()
    except Exception as e:
        print("Error occured when checking availability")
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()
    # Check available vaccines
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)
    check_vaccine = "SELECT * FROM Vaccines"
    try:
        cursor.execute(check_vaccine)
        results_vaccine = cursor.fetchall()
        print()
        if len(results_vaccine) == 0:
            print("No avaliable vaccine currently")
        else:
            print("Here are avaliable vaccines and its doses:")
            for row in results_vaccine:
               print("{} : {} dose(s) available.".format(row['Name'], row['Doses']))
    except pymssql.Error as E:
        print("Error occurred when checking vaccines")
        print("Please try again!")
        print("Db-Error:", E)
        quit()
    except Exception as e:
        print("Error occured when checking vaccines")
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()
    return results_caregivers,results_vaccine


def reserve(tokens):
    """
    reserve <date> <vaccine> <caregiver>
    Patient researves a vaccine appointment on a given date and caregiver.
    Return an appointment ID, assgined caregiver if success,
    or return error message.
    Part 2 Finished.
    """
    global current_patient
    global current_caregiver
    # Check token and current user
    if len(tokens) != 4:
        print("Invalid args. Please try again")
        return
    if current_patient is None and current_caregiver is None:
        print("Please login first!")
        return
    if current_caregiver is not None and current_patient is None:
        print("Please login as patient!")
        return
    date = tokens[1]
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    # Check if input date is valid
    try:
        d = datetime.datetime(year, month, day)
    except ValueError as e:
        print("Invalid date:", e)
        print("Please try again!")
        return
    # Check available caregiver and dose:
    results_caregiver = None
    results_vaccine = None
    vaccine = tokens[2]
    caregiver = tokens[3]
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)
    check_caregiver = "SELECT * FROM Availabilities WHERE Time = %s \
                       AND Username = %s"
    check_vaccine = "SELECT * FROM Vaccines WHERE Name = %s"
    try:
        cursor.execute(check_caregiver, (d, caregiver))
        results_caregiver = cursor.fetchall()
        cursor.execute(check_vaccine, vaccine)
        results_vaccine = cursor.fetchall()
        if len(results_caregiver) == 0:
            print("Your selected caregiver is unavailable!")
            print("Please try again!")
            return
        if len(results_vaccine) == 0:
            print("Sorry we currently do not have {} vaccine.".format(vaccine))
            print("Please try again!")
            return
        if results_vaccine[0]['Doses'] == 0:
            print("Sorry currently {} vaccine is out of stock now".format(vaccine))
            return
           # update Availabilities table
    except pymssql.Error as E:
        print("Error occurred when checking available caregivers")
        print("Please try again!")
        print("Db-Error:", E)
        quit()
    except Exception as e:
        print("Error occured when checking availability")
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()
    # Assign caregiver, update availability, vaccine and insert into appointment
    appointed_caregiver = caregiver
    delete_availability = "DELETE FROM Availabilities WHERE Username = %s and Time = %s"
    decrease_dose = "UPDATE vaccines SET Doses = %d WHERE Name = %s"
    add_appointment = "INSERT INTO Appointments VALUES (%s, %s, %s, %s)"
    para = (str(d)[:10], appointed_caregiver, str(current_patient.username), vaccine)
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)
    try:
        cursor.execute(delete_availability, (appointed_caregiver, d))
        cursor.execute(decrease_dose, (results_vaccine[0]['Doses'] - 1, vaccine))
        cursor.execute(add_appointment, para)
        conn.commit()
        cursor.execute("SELECT Id FROM Appointments WHERE Time = %s \
                        AND Caregiver_name = %s AND Patient_name = %s \
                        AND Vaccine_name = %s", para)
        reserve_result = cursor.fetchall()
        appoint_id = reserve_result[0]['Id']
    except pymssql.Error as E:
        print("Error occurred when updating tables")
        print("Please try again!")
        print("Db-Error:", E)
        quit()
    except Exception as e:
        print("Error occured when updating tables")
        print("Please try again!")
        return
    finally:
        cm.close_connection()
    print("Appointment ID: {}, Caregiver.name : {}".format(appoint_id, appointed_caregiver))
    return reserve_result


def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.date(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    return


def cancel(tokens):
    """
    Patient or caregiver cancels an successful appointment with its unique ID.
    Part 2 Finished.
    """
    global current_patient
    global current_caregiver
    # Check current user
    if current_patient is None and current_caregiver is None:
        print("Please login first!")
        return
    if len(tokens) != 2:
        print("Invalid args. Please try again")
        return
    appoint_id = tokens[1]
    check_appoint = "SELECT Time, Caregiver_name, Patient_name, Vaccine_name \
                    FROM Appointments WHERE Id = %s"
    delete_appoint = "DELETE FROM Appointments WHERE Id = %s"
    insert_availability = "INSERT INTO Availabilities VALUES (%s, %s)"
    check_vaccine = "SELECT Doses FROM Vaccines WHERE Name = %s"
    increase_doses = "UPDATE Vaccines SET Doses = %d WHERE name = %s"
    # Get the appointment info of the given appointment ID,
    # Delete the appointment entry, and update availabilities, vaccines table.
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)
    try:
        cursor.execute(check_appoint, appoint_id)
        results_dict = cursor.fetchall()
        if len(results_dict) == 0:
            print("Invalid appointment Id. Please try again!")
            return
        results = results_dict[0]
        (date,caregiver,patient,vaccine) = (results['Time'], results['Caregiver_name'], results['Patient_name'],results['Vaccine_name'])
        if current_patient is not None and current_patient.username != patient:
            print("Incorrect appointment Id. Please try again!")
            return
        if current_caregiver is not None and current_caregiver.username != caregiver:
            print("Incorrect appointment Id. Please try again!")
            return
        cursor.execute(delete_appoint, appoint_id)
        cursor.execute(insert_availability, (str(date)[:10], caregiver))
        cursor.execute(check_vaccine, vaccine)
        curr_doses = cursor.fetchall()[0]['Doses']
        cursor.execute(increase_doses, (curr_doses + 1, vaccine))
        conn.commit()
    except pymssql.Error as E:
        print("Error occurred when cancelling appointments")
        print("Please try again!")
        print("Db-Error:", E)
        quit()
    # except Exception as e:
    #     print("Error occured when cancelling appointments")
    #     print("Please try again!")
    #     print("Error:", e)
    #     return
    finally:
        cm.close_connection()
    print("Successfully cancelled appointment.")


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    '''
    Show appointments that have been assigned to the current login patient or caregiver.
    Return appointment ID, vaccine name, date, caregiver name for each appointment.
    Part 2 Finished.
    '''
    global current_caregiver
    global current_patient
    if current_patient is None and current_caregiver is None:
        print("Please login first!")
        return
    elif current_patient is not None and current_caregiver is None:
         check_appoint = "SELECT Id, Vaccine_name, Time, Caregiver_name \
                         FROM Appointments WHERE Patient_name = %s ORDER BY Id ASC"
         cm = ConnectionManager()
         conn = cm.create_connection()
         cursor = conn.cursor(as_dict=True)
         try:
             cursor.execute(check_appoint, current_patient.username)
             results = cursor.fetchall()
             if len(results) == 0:
                 print("No appointmented found. Please try again!")
                 return
             else:
                 for row in results:
                     print("Appointment ID: {}, Vaccine Name: {}, Date: {}, Caregiver Name: {}.".format(row['Id'], row['Vaccine_name'], row['Time'], row['Caregiver_name']))
         except pymssql.Error as E:
             print("Error occurred when checking appointments")
             print("Db-Error:", E)
             quit()
         except Exception as e:
             print("Error occurred when checking appointments")
             print("Error:", e)
             return
         finally:
             cm.close_connection()
    elif current_caregiver is not None and current_patient is None:
         check_appoint = "SELECT Id, Vaccine_name, Time, Patient_name \
                         FROM Appointments WHERE Caregiver_name = %s ORDER BY Id ASC"
         cm = ConnectionManager()
         conn = cm.create_connection()
         cursor = conn.cursor(as_dict=True)
         try:
             cursor.execute(check_appoint, current_caregiver.username)
             results = cursor.fetchall()
             if len(results) == 0:
                 print("No appointmented found. Please try again!")
                 return
             else:
                 for row in results:
                     print("Appointment ID: {}, Vaccine Name: {}, Date: {}, Patient Name: {}.".format(row['Id'], row['Vaccine_name'], row['Time'], row['Patient_name']))
         except pymssql.Error as E:
             print("Error occurred when checking appointments")
             print("Db-Error:", E)
             quit()
         except Exception as e:
             print("Error occurred when checking appointments")
             print("Error:", e)
             return
         finally:
             cm.close_connection()
    else:
        print("You have login as both patient and caregiver. Please log out and try again!")
    return


def logout(tokens):
    """
    Logout the current user identity.
    Part 2 Finished
    """
    global current_caregiver
    global current_patient
    try:
        if current_patient is None and current_caregiver is None:
            print("Please login first!")
        else:
            current_patient = None
            current_caregiver = None
            print("Successfully logged out!")
    except pymssql.Error as E:
            print("Error occurred when checking appointments")
            print("Db-Error:", E)
            quit()
    except Exception as e:
            print("Error occurred when checking appointments")
            print("Error:", e)
            return
    return


def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")
    print("> reserve <date> <vaccine>")
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")
    print("> logout")
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')
        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break
        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == "cancel":
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
