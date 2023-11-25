from PySide6.QtWidgets import QApplication

from MainApplication import MainApplication
from SignUpDialog import SignUpDialog


class Application:
    def __init__(self, args=None) -> None:
        self.app = QApplication(args)

        with open("style.css") as file:
            lines: list[str] = file.readlines()
            stylesheet = ""
            for line in lines:
                stylesheet += line
            self.app.setStyleSheet(stylesheet)

        self.mainApp = None
        self.signUp = SignUpDialog()
        self.signUp.successfullySignedUp.connect(self.startMainApplication)

    def start(self) -> int:
        self.signUp.open()
        return self.app.exec()

    def startMainApplication(self, email: str) -> None:
        self.mainApp = MainApplication(email)
        self.mainApp.show()
