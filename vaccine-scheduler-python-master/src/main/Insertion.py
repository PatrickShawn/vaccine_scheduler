from scheduler import *

# Create 5 patients. To simply, set their password to 123456 as default
Patient_list = ['Bob','Derick','Jessica','Justin','Patrick', "Lily", "Ben", "Lee", "Jo", "Tyler"]
for i in Patient_list:
    token = ['', '123456']
    token.insert(1, i)
    create_patient(token)

# Create 3 Caregivers. To simply, set their password to 654321 as default
Caregiver_list = ['CVS', 'Walgreen', 'MinuteClinic', "Ann", "Michael", "Jannet", "Maria", "Sara", "Kay", "Penny"]
for i in Caregiver_list:
    token = ['', '654321']
    token.insert(1, i)
    create_caregiver(token)

Vaccine_dict = {'Pfizer' : 30, 'Moderna' : 40, 'Flu' : 50, 'Tdap' : 60, "Hepatitis_A": 10,
                "Hepatitis B": 10, "HPV" : 20, "MMR": 40, "Rabies" : 10, "Typhoid": 20}
Avaliability_dict = {'CVS': ['6-1-2023', '6-2-2023', '6-3-2023'],
                     'Walgreen' : ['6-1-2023', '6-2-2023', '6-6-2023', '6-9-2023'],
                     'MinuteClinic' : ['6-7-2023', '6-8-2023', '6-9-2023'],
                     "Ann" : ['6-7-2023', '6-8-2023', '6-9-2023'],
                     "Michael" : ['6-10-2023'], "Jannet" : ['6-10-2023'],
                     "Maria" : ['6-11-2023'], "Sara" : ['6-9-2023', '6-11-2023'],
                     "Kay" : ['6-15-2023'], "Penny" : ['6-14-2023']}
# For each caregiver, upload their vaccine doses and avaliability.
for cg in Caregiver_list:
    # First, login in as caregiver
    login_caregiver(['', cg, '654321'])
    # Upload their vaccince doses. To simplify, assume each caregiver has the same
    # doses for each vaccine
    for v in Vaccine_dict:
        add_doses(['', v, Vaccine_dict[v] / len(Caregiver_list)])
        # Upload their avaliability.
    for date in Avaliability_dict[cg]:
        upload_availability(['', date])
    # Logout
    logout("")
