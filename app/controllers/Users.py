
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.db = self._app.db

   
    def index(self):
        return self.load_view('index.html')

    def display_login_reg(self):
        if 'val_errors' in session:
            for error in session['val_errors']:
                flash(error)
            session.pop('val_errors')
        return self.load_view('index.html')

    def register(self):
  
        validation_result = self.models['User'].validate_reg_info(request.form)

        return self.handle_login_reg_response(validation_result)

    def handle_login_reg_response(self, result):
        if type(result) == list:
            session['val_errors'] = result
            return redirect('/')
        self.set_user_session(result)
        return redirect('/success')
    def login(self):
        login_result = self.models['User'].login(request.form)
        return self.handle_login_reg_response(login_result)

    def logout(self):
        session.clear()
        return redirect('/')

    def set_user_session(self, validation_result):
        session['user'] = validation_result
        return

    def success(self):
        name = self.models['User'].fetch_user_by_id(id)
        return self.load_view('success.html', name=name)


