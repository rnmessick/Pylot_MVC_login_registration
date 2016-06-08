
from system.core.model import Model
from flask import session, request
from flask.ext.bcrypt import Bcrypt

class User(Model):
    def __init__(self):
        super(User, self).__init__()


    def registration(self):
        user_info = {
        "first_name" : request.form['first_name'], 
        "last_name" : request.form['last_name'], 
        "email" : request.form['email'], 
        }
        password = request.form['password']
    # run validations and if they are successful we can create the password hash with bcrypt
        pw_hash = self.bcrypt.generate_password_hash(password)
    # now we insert the new user into the database
        create_query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at) VALUES (:first_name, :last_name, :email, :pw_hash, NOW(), NOW())"
        create_data = { 'first_name': request.form['first_name'], 'last_name':request.form['last_name'], 'email': request.form['email'], 'pw_hash': pw_hash }
        self.db.query_db(create_query, create_data)

    def register_validation(self, form):
        if len(request.form['first_name']) < 2 or len(request.form['last_name']) < 2:
            flash("Name must be greater than 2 letters!")
            return redirect("/")
        if (request.form['first_name']).isalpha() == False or (request.form['last_name']).isalpha() == False:
            flash("Name cannot contain any numbers.")
        if len(request.form["email"]) < 1:
            flash("Email cannot be blank!")
        elif not EMAIL_REGEX.match(request.form["email"]):
            flash("Invalid Email Address!")
        if len(request.form["password"]) < 8:
            flash("Invalid Password. Try again.")
        elif (request.form["password"]) != (request.form["confirm"]):
            flash("Passwords do not match.")
        else:
            # Code to insert user goes here...
            # Then retrieve the last inserted user.
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return { "status": True, "user": users[0] }

       

    def login(self, form):
        email = request.form['email']
        password = request.form['password']
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = { 'email': request.form['email'] }
        user = self.db.query_db(user_query, user_data).fetchone()
        if user:

            if bcrypt.check_password_hash(user.pw_hash, password):
                return user
        else:
            flash("Invalid Password. Please try again.")
        
        return False