
from system.core.model import Model
import re

EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()
        self.validation_errors = {
            'name_exist' : "Name can't be blank",
            'email_exist' : "Email can't be blank",
            'email_valid' : "Email must be valid.",
            'password_exist' : "Password can't be blank",
            'password_match' : "Passwords must match",
            'email_taken' : "Email already in use",
            'login_fail' : "Email/password don't match"
        }
        self.queries = {
            'get_user_by_email' : "SELECT * FROM users WHERE email = :email LIMIT 1",
            'create_user' : "INSERT INTO users (name, alias, email, pw_hash, created_at, updated_at) VALUES ( :name, :alias, :email, :pw_hash, NOW(), NOW())",
            'fetch_user_by_id': "SELECT id, name, alias, email FROM users WHERE id = :id",
            'fetch_all_users' : "SELECT id, name, alias, email, created_at FROM users WHERE id != :id"
        }

    def register(self, form_data):
        # Encrypt password
        pw_hash = self.bcrypt.generate_password_hash(form_data['password'])

        # Make a DB query to create a user
        query = self.queries['create_user']
        data = {
            'name' : form_data['name'],
            'alias' : form_data['alias'],
            'email' : form_data['email'],
            'pw_hash' : pw_hash
        }

        result = self.db.query_db(query, data)

        return self.fetch_user_by_id(result)


    def validate_reg_info(self, form_data):
        errors = []

        if len(form_data['name']) < 1:
            errors.append(self.validation_errors['name_exist'])
        if len(form_data['email']) < 1:
            errors.append(self.validation_errors['email_exist'])
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append(self.validation_errors['email_valid'])
        if len(form_data['password']) < 1:
            errors.append(self.validation_errors['password_exist'])
        if form_data['password'] != form_data['password_confirm']:
            errors.append(self.validation_errors['password_match'])

        # Do errors exists? If so, don't both with DB query...
        if len(errors) > 0:
            return errors

        result = self.get_user_by_email(form_data['email'])

        if len(result) > 0:
            errors.append(self.validation_errors['email_taken'])
            return errors

        # If we're here, we know all validations passed
        return self.register(form_data)

    def fetch_user_by_id(self, id):
        query = self.queries['fetch_user_by_id']
        data = { 'id' : id }
        result = self.db.query_db(query, data)
        return result
        
    def get_user_by_email(self, email):
        query = self.queries['get_user_by_email']
        data = { 'email' : email }
        return self.db.query_db(query, data)      

    def login(self, form_data):
        result = self.get_user_by_email(form_data['email'])

        password = form_data['password']
        pw_hash = result[0]['pw_hash']

        test_password_result = self.bcrypt.check_password_hash(pw_hash, password)

        if test_password_result == False:
            return [self.validation_errors['login_fail']]
        else:
            return {
                'id' : result[0]['id'],
                'name' : result[0]['name'],
                'email' : result[0]['email'],

            }