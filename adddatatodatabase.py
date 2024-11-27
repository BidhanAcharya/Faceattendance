import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("put here path  of the json file")
firebase_admin.initialize_app(cred,{
    "databaseURL": "https://yourfirebasename-9726a-default-rtdb.firebaseio.com/"
    
})
## students is the root node which will be created in the database
ref = db.reference('students')
data = {
    "12345": {
        "name": "Bidhan Acharya",
        "email": "hello@gmail.com",
        "student": "CSE"
         
    },     ## make sure the unique key of the student and image name of student is same . Similarly you can add other students details
     
    
    
}
for key,value in data.items():
    ref.child(key).set(value)
    
print("Data has been stored")