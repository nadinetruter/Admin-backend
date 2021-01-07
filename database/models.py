from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


#class for admin to fill in the rest of their profile details
# added_by is to tell the program which user added the admin info
class Admin(db.Document):
    name = db.StringField(required=True)
    surname = db.StringField(required=True)
    gender = db.StringField(required= False)
    id_number = db.StringField(required = False)
    address = db.StringField(required=False)
    city = db.StringField(required=False)
    country = db.StringField(required=False)
    postal_code = db.StringField(required=False)
    phone_number =db.StringField(required=False)
    primary = db.BooleanField(required = False)
    added_by = db.ReferenceField('SignUp')



# class for admins to signup/create an account
# added hash password so that password is stored in the db as a secret key
class SignUp(db.Document):
    name = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    admin = db.ListField(db.ReferenceField('Admin', reverse_delete_rule=db.PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


#if a user is deleted then the movie created by the user is also deleted.
SignUp.register_delete_rule(Admin, 'added_by', db.CASCADE)
