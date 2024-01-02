import firebase_admin
from firebase_admin import credentials
from firebase_admin import  db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://smartattendance-2e574-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    '416':
        {
            'name':' Jack Sgsjthaerklparrow',
            'branch':'ECE',
            'starting_year':2020,
            'total_attendance':7,
            'year':4,
            'last_attendance_time':'2023-12-11 00:54:35'
        },
    '420':
        {
            'name':'Nani',
            'branch':'CSE',
            'starting_year':2020,
            'total_attendance':8,
            'year':4,
            'last_attendance_time':'2023-12-11 00:25:35'
        },
    '425':
        {
            'name':'Nadella',
            'branch':'CSE DS',
            'starting_year':2022,
            'total_attendance':6,
            'year':2,
            'last_attendance_time':'2023-12-11 00:54:35'
        },
    '451':
        {
            'name':'SuryaKumar Yadav',
            'branch':'ECE',
            'starting_year':2021,
            'total_attendance':6,
            'year':3,
            'last_attendance_time':'2022-12-11 00:54:35'
        }

}


for key,value in data.items():
    ref.child(key).set(value)