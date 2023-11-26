# PySide6/Qt

## What is PySide6?

PySide6 is a Python module that allows you to use the Qt framework to create graphical user interfaces (GUIs) in Python.\
Qt was originally developed by Trolltech, in 1990. It is now developed by The Qt Company, a subsidiary of Digia.

## How to use PySide6

PySide6 can be installed using pip:

```bash
pip install PySide6
```

After having installed the module, you can start using it in your Python code.

### Hello World Example

To build a basic Hello World GUI application using PySide6, you will need to import two classes. QApplication and QLabel.

The QApplication class is the base of our application. It will manage the controls and the main settings of the application.

The QLabel class in this example is a simple widget that shows the "Hello World" text.

Qt is a widget-based framework. Every widget is a subclass of QWidget.

```python
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication()
label = QLabel("Hello World!")
label.show()
app.exec_()
```

### Widgets

Qt has a lot of widgets that can be used to build your GUI. It basically provides every basic visual element you can think of. It has buttons, text boxes, sliders, etc.

In my application, I used the following widgets:

- QLabel
- QPushButton
- QListWidget
- QLineEdit
- QComboBox
- QScrollArea

I will talk a bit about each of these widgets.

#### QLabel

The QLabel widget is a simple widget that can display text or an image.
In my application I use it to display the images of the meals, and also all of the text throughout the application.

#### QPushButton

The QPushButton widget is a button that can be clicked by the user. You can customize what kind of text is displayed on the button, and what happens when the button is clicked. \
In Qt, you have connections that handle the events such as pressing a button. You can connect a button to a function, and when the button is pressed, the function will be called. \
This could look something like this:

```python
button = QPushButton("Click me!")
button.clicked.connect(my_function)

def my_function():
    print("Button was clicked!")
```

#### QListWidget

The QListWidget widget is used to displays a list of items. By default, it displays a vertical list of strings. \
In my application, I use it to display the list of search results.

QListWidget inherits from the QListView class, which is a widget that displays items from a model. Developers can provide their own models to display their own data and they can customize the appearance of the view.

#### QLineEdit

The QLineEdit widget is a widget that allows the user to enter and edit a single line of plain text. \
I use it in my application to allow the user to enter their email, password, and to enter a search query.

These QLineEdit widgets can be customized to only allow certain types of input. For example, you can make it so that the user can only enter numbers, or only letters. You can also use regular expressions to validate the input in a QLineEdit.

You can also customize these widgets to not show the input. This is useful for password fields. \
I did this for the password field in my application with the following code:

```python
password_field = QLineEdit()
password_field.setEchoMode(QLineEdit.Password)
```

#### QComboBox

The QComboBox widget is a widget that allows the user to select an item from a list of items. \
I use it in my application to allow the user to select the category for the search query. \
A combo box is also known as a drop-down menu.

#### QScrollArea

The QScrollArea widget provides a scrolling view around another widget. \
This is useful if you have another widget with a lot of content, and you want to be able to scroll through it. \
I use it in my application to display the ingredients of a meal and the instructions to prepare that meal.

### Layouts

Qt has a lot of different layouts that can be used to arrange the widgets in your application. \
Layouts are used to arrange widgets in a certain way. For example, you can use a layout to arrange the widgets in a grid, or in a horizontal or vertical line. \
I only used QHBoxLayout and QVBoxLayout in my application. These are layouts that align widgets horizontally or vertically.

## Why I wanted to use PySide6

I wanted to use a GUI library since I always loved the idea of front-end programming. I like how when creating a front-end application you instantly get rewarded by being able to see what effect your code has right in front of you. \
I thought Qt for Python was going to be a simple way of exploring front-end programming, and I was right. It is really easy to create an application using PySide6 and it is very enjoyable.

## My learnings

Playing around with the PySide6 library has primarily helped understand the object-oriented part of Python. This is because every Widget is a class, and you can inherit from every widget. You can modify them as you wish and really make them yours.

## My experience with PySide6

I really enjoyed creating a GUI application with PySide6 and I would certainly like to continue using it in the future to create small GUI applications. I am not sure about how big you can make the applications before the structure gets really confusing. \
I would recommend this library to anyone that wants to create their first GUI application since it is so easy to understand. I would also recommend it to anyone that just needs to create a quick GUI application for a small project.

## Resources

[Qt History](https://wiki.qt.io/Qt_History)\
[PyPi PySide6](https://pypi.org/project/PySide6/)
[Your first PySide6 application](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/widgets.html)
[PySide6 Documentation](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html#module-PySide6.QtWidgets) \
