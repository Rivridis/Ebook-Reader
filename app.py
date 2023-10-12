from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout,QMessageBox,QLineEdit,QPushButton
from PySide6.QtUiTools import QUiLoader
import qdarktheme

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Load the .ui file
        loader = QUiLoader()
        ui_file = "assets/login.ui" 
        ui = loader.load(ui_file, self)

        self.setFixedSize(650, 350)

        # Accessing the QLineEdit widgets
        self.user_input = ui.findChild(QLineEdit, "user")
        self.pass_input = ui.findChild(QLineEdit, "pass")

        # Connect the login button to the login method
        self.login_button = ui.findChild(QPushButton, "Login")
        self.login_button.clicked.connect(self.login)

        self.signup_button = ui.findChild(QPushButton, "Signin")
        self.signup_button.clicked.connect(self.switch_to_signup)


    def login(self):
        user = self.user_input.text()
        passw = self.pass_input.text()

        if user == 'admin' and passw == 'password':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Login Successful")
            msg.setWindowTitle("Success")
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Invalid Username or Password")
            msg.setWindowTitle("Error")
            msg.exec()
    
    def switch_to_signup(self):
        self.close()
        signup_dialog = SignupDialog()
        signup_dialog.exec()

class SignupDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Load the .ui file
        loader = QUiLoader()
        ui_file = "assets/signup.ui" 
        ui = loader.load(ui_file, self)

        self.setFixedSize(650, 350)

        # Accessing the QLineEdit widgets for signup page
        self.user_input = ui.findChild(QLineEdit, "user")
        self.pass_input = ui.findChild(QLineEdit, "pass")

        # Connect the signup button to the signup method
        self.signup_button = ui.findChild(QPushButton, "Login")
        self.signup_button.clicked.connect(self.signup)

    def signup(self):
        user = self.user_input.text()
        passw = self.pass_input.text()
        self.switch_to_login()

    def switch_to_login(self):
        self.close()
        login_dialog = LoginDialog()
        login_dialog.exec()

app = QApplication([])
qdarktheme.setup_theme()

# Create and show the login dialog
login_dialog = LoginDialog()
login_dialog.exec()

# Start the application event loop
app.exec()

    


