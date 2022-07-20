
import re
from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint
from flask_app import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'login_and_reg'

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append( User(user) )
        return users
    
    @classmethod
    def get_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:
            return False
        else:
            user = result[0]
        return User(user)
        
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # validations for saving are done inside of our classmethod 

    @staticmethod
    def validate_user(user):
        is_valid = True
        if user['password'] != user['password_confirmation']:
            flash("passwords do not match", "confirmation")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("first name is too short ", "first_name")
            is_valid = False 
        if len(user['last_name']) < 2:
            flash("last name is too short ", "last_name")
            is_valid = False 
        if len(user['password']) < 8:
            flash("password is too short ", "email")
            is_valid = False 
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid
    
    # now we call this in our register users controller


