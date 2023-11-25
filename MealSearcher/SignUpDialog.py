from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, Qt, QPainter, QIcon
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication

from Formatting import check_email, check_password


class SignUpDialog(QDialog):
    badPasswordCount: int = 0
    successfullySignedUp = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        icon_pixmap = QPixmap(20, 20)
        icon_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(icon_pixmap)
        painter.drawText(icon_pixmap.rect(), Qt.AlignmentFlag.AlignCenter, ":)")
        painter.end()
        self.setWindowIcon(QIcon(icon_pixmap))

        self.setWindowTitle("Sign Up")

        titleLabel = QLabel("Sign up to Recipe Searcher")
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titleLabel.setStyleSheet("QLabel{ font-size:30px; }")

        self.disclosureLabel = QLabel("(This isn't a real sign up form, just enter any email and a secure password.)")
        self.disclosureLabel.setWordWrap(True)
        self.disclosureLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.emailLineEdit = QLineEdit(self)
        self.emailLineEdit.setPlaceholderText("Email")
        self.emailLineEdit.setMinimumHeight(30)

        self.passwordLineEdit = QLineEdit(self)
        self.passwordLineEdit.setPlaceholderText("Password")
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwordLineEdit.setMinimumHeight(30)

        self.loginButton = QPushButton("Sign Up!!!", self)
        self.loginButton.clicked.connect(self.buttonPressed)
        self.loginButton.setMinimumHeight(30)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(titleLabel)
        self.layout.addWidget(self.disclosureLabel)
        self.layout.addWidget(self.emailLineEdit)
        self.layout.addWidget(self.passwordLineEdit)
        self.layout.addWidget(self.loginButton)

    def buttonPressed(self):
        self.loginButton.setDisabled(True)

        try:
            email = self.emailLineEdit.text()
            if not check_email(email):
                self.emailLineEdit.setStyleSheet('QLineEdit{border: 1px solid red;}')
                raise Exception("Bad email")
            else:
                self.emailLineEdit.setStyleSheet('QLineEdit{border: 1px solid black;}')

            password = self.passwordLineEdit.text()
            if not check_password(password):
                self.badPasswordCount += 1
                self.disclosureLabel.setStyleSheet("QLabel {color: darkred;}")
                if self.badPasswordCount == 1:
                    self.disclosureLabel.setText(
                        ("I said a secure password! That's 8 characters, one uppercase, one lowercase, "
                         "one number, and one special character. Not THAT hard..."))
                elif self.badPasswordCount == 2:
                    self.disclosureLabel.setText(
                        "Alright come on, make an effort now. Something more secure than that.")
                elif self.badPasswordCount == 3:
                    self.disclosureLabel.setText("... really?")
                elif self.badPasswordCount > 3:
                    QApplication.exit(2)

                raise Exception("Bad password")

            self.successfullySignedUp.emit(email)
            self.close()

        except Exception as e:
            print(e)
        finally:
            self.loginButton.setEnabled(True)
