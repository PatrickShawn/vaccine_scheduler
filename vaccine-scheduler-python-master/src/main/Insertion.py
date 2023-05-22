from scheduler import *

# Create 5 patients. To simply, set their password to 123456 as default
Patient_list = ['Bob', 'Derick', 'Jessica', 'Justin', 'Patrick']
for i in Patient_list:
    token = ['', '123456']
    token.insert(1, i)
    create_patient(token)

# Create 3 Caregivers. To simply, set their password to 654321 as default
Caregiver_list = ['CVS', 'Walgreen', 'MinuteClinic']
for i in Caregiver_list:
    token = ['', '654321']
    token.insert(1, i)
    create_caregiver(token)

Vaccine_dict = {'Pfizer' : 27, 'Moderna' : 21, 'Flu' : 30, 'Tdap' : 15}
Avaliability_dict = {'CVS': ['6-1-2023', '6-2-2023', '6-3-2023'],
                     'Walgreen' : ['6-4-2023', '6-5-2023', '6-6-2023'],
                     'MinuteClinic' : ['6-7-2023', '6-8-2023', '6-9-2023']}
# For each caregiver, upload their vaccine doses and avaliability.
for cg in Caregiver_list:
    # First, login in as caregiver
    login_caregiver(['', cg, '654321'])
    # Upload their vaccince doses. To simplify, assume each caregiver has the same
    # doses for each vaccine
    for v in Vaccine_dict:
        add_doses(['', v, Vaccine_dict[v] / 3])
        # Upload their avaliability.
    for date in Avaliability_dict[cg]:
        upload_availability(['', date])
    # Logout
    logout("")
