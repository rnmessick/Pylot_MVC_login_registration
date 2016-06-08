
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.db = self._app.db

   
    def index(self):
        return self.load_view('index.html')

    def registration(self):
        user_info = {
        "first_name" : request.form['first_name'], 
        "last_name" : request.form['last_name'], 
        "email" : request.form['email'], 
        "password" : request.form['password']
        }
        self.models['User'].registration()
        return redirect('/')

    def login(self):
        user_info = {
        "first_name" : request.form['first_name'], 
        "last_name" : request.form['last_name'], 
        "email" : request.form['email'], 
        }
        self.models['User'].login(user_info)
        return redirect('/success')

    def success(self):
        email = request.form['email']
        return self.load_view('success.html', email=email)


