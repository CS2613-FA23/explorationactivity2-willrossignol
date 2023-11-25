from enum import Enum
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, Qt, QPainter, QIcon, QImage
from PySide6.QtWidgets import QWidget, QMainWindow, QComboBox, QLineEdit, QPushButton, QListWidget, \
    QHBoxLayout, QVBoxLayout, QListWidgetItem, QDockWidget, QLabel, QScrollArea

from APICalls import get_random_meals, search_by_name, search_by_main_ingredient, search_by_category, \
    search_by_area, download_picture, get_meal_by_id


class SearchTypes(str, Enum):
    NAME = 'Meal Name'
    CATEGORY = "Category"
    AREA = "Area"
    INGREDIENT = "Main Ingredient"


class MainApplication(QMainWindow):
    def __init__(self, userEmail: str, parent: QWidget = None):
        super().__init__(parent)

        self.userEmail = userEmail

        self.setWindowTitle("Meal Searcher")

        self.setMinimumHeight(500)

        iconPixmap = QPixmap(20, 20)
        iconPixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(iconPixmap)
        painter.drawText(iconPixmap.rect(), Qt.AlignmentFlag.AlignCenter, ":)")
        painter.end()
        self.setWindowIcon(QIcon(iconPixmap))

        self.searchingWidget = SearchingWidget(self)
        self.setCentralWidget(self.searchingWidget)

        self.detailsDock = MealDetailsDockWidget(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.detailsDock)

        self.searchingWidget.updateShownMeal.connect(self.detailsDock.updateInformation)


class SearchingWidget(QWidget):
    updateShownMeal = Signal(dict)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        appTitleLabel = QLabel("Meal Searcher", self)
        appTitleLabel.setStyleSheet(appTitleLabel.styleSheet() + "QLabel{font-size: 24px;}")

        self.searchTypeCombo = QComboBox(self)
        self.searchTypeCombo.addItems(
            [SearchTypes.NAME, SearchTypes.INGREDIENT, SearchTypes.CATEGORY, SearchTypes.AREA])
        self.searchLineEdit = QLineEdit(self)
        self.searchLineEdit.setPlaceholderText("Input search term here...")
        self.searchButton = QPushButton("Search", self)
        self.searchButton.clicked.connect(self.searchButtonPressed)
        self.randomButton = QPushButton("Suprise Me!", self)
        self.randomButton.clicked.connect(lambda: self.populateMealList(get_random_meals()))

        self.resultsView = QListWidget(self)
        self.resultsView.currentItemChanged.connect(self.listChoiceChanged)

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchTypeCombo)
        searchLayout.addWidget(self.searchLineEdit)
        searchLayout.addWidget(self.searchButton)
        searchLayout.addWidget(self.randomButton)

        root = QVBoxLayout(self)
        root.addWidget(appTitleLabel)
        root.addLayout(searchLayout, 0)
        root.addWidget(self.resultsView, 1)

    def searchButtonPressed(self):
        searchType = self.searchTypeCombo.currentText()
        searchInput = self.searchLineEdit.text()
        response = None
        if searchType == SearchTypes.NAME:
            response = search_by_name(searchInput)
        elif searchType == SearchTypes.INGREDIENT:
            response = search_by_main_ingredient(searchInput)
        elif searchType == SearchTypes.CATEGORY:
            response = search_by_category(searchInput)
        elif searchType == SearchTypes.AREA:
            response = search_by_area(searchInput)
        else:
            print("ERROR: searchType not recognized")
            return

        if response is None:
            print("ERROR: Bad response")
            self.resultsView.clear()
            return

        self.populateMealList(response)

    def listChoiceChanged(self, new: QListWidgetItem, old: QListWidgetItem):
        if new is None:
            self.updateShownMeal.emit(None)
        else:
            if self.searchTypeCombo.currentText() != SearchTypes.NAME:
                meal = get_meal_by_id(new.data(Qt.ItemDataRole.UserRole).get("idMeal"))
                self.updateShownMeal.emit(meal)
            else:
                self.updateShownMeal.emit(new.data(Qt.ItemDataRole.UserRole))

    def populateMealList(self, mealsList: list[dict]):
        self.resultsView.clear()

        for meal in mealsList:
            item = QListWidgetItem(meal.get("strMeal"))
            item.setData(Qt.ItemDataRole.UserRole, meal)
            self.resultsView.addItem(item)


class MealDetailsDockWidget(QDockWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setMinimumWidth(300)

        widget = QWidget(self)
        self.setWidget(widget)

        title = QLabel("Meal Details", widget)
        title.setStyleSheet(title.styleSheet() + 'QLabel {font-size: 24px;}')
        self.imageLabel = QLabel(widget)
        self.imageLabel.hide()
        self.imageLabel.setFixedHeight(200)
        self.imageLabel.setFixedWidth(200)
        self.imageLabel.setScaledContents(True)

        self.mealLabel = QLabel("No Meal Selected", widget)
        self.mealLabel.setStyleSheet(self.mealLabel.styleSheet() + 'QLabel {font-size: 18px;}')
        self.mealLabel.setWordWrap(True)

        self.areaLabel = QLabel("Area: N/A", widget)
        self.categoryLabel = QLabel("Category: N/A", widget)
        areaCategoryLayout = QHBoxLayout()
        areaCategoryLayout.addWidget(self.areaLabel, 0, Qt.AlignmentFlag.AlignCenter)
        areaCategoryLayout.addSpacing(20)
        areaCategoryLayout.addWidget(self.categoryLabel, 0, Qt.AlignmentFlag.AlignCenter)
        areaCategoryLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ingredientsHeader = QLabel("Ingredients:")
        ingredientsHeader.setStyleSheet(ingredientsHeader.styleSheet() + 'QLabel {font-size:14px;}')
        self.ingredientsScrollArea = QScrollArea(widget)
        instructionsScrollArea = QScrollArea(widget)

        instructionsHeader = QLabel("Instructions:")
        instructionsHeader.setStyleSheet(instructionsHeader.styleSheet() + 'QLabel {font-size:14px;}')
        self.instructionsLabel = QLabel("")
        self.instructionsLabel.setWordWrap(True)
        instructionsScrollArea.setWidget(self.instructionsLabel)
        instructionsScrollArea.setWidgetResizable(True)

        layout = QVBoxLayout(widget)
        layout.addWidget(title)
        layout.addWidget(self.imageLabel)
        layout.addWidget(self.mealLabel)
        layout.addLayout(areaCategoryLayout)
        layout.addWidget(ingredientsHeader)
        layout.addWidget(self.ingredientsScrollArea)
        layout.addWidget(instructionsHeader)
        layout.addWidget(instructionsScrollArea)

    def updateInformation(self, data: dict):
        if data is None:
            self.imageLabel.hide()
            self.mealLabel.setText("No Meal Selected")
            self.areaLabel.setText("Area: N/A")
            self.categoryLabel.setText("Category: N/A")
            return

        ingredients = self.__parseIngredients(data)
        ingredientsWidget = MealIngredientsWidget(ingredients)
        self.ingredientsScrollArea.setWidget(ingredientsWidget)

        thumbnail = data.get('strMealThumb')
        if thumbnail and download_picture(thumbnail):
            picture = QImage("./temp/picture.jpg")
            self.imageLabel.setPixmap(QPixmap.fromImage(picture))
            self.imageLabel.show()

        self.mealLabel.setText(data.get('strMeal'))
        self.categoryLabel.setText(f"Category: {data.get('strCategory')}")
        self.areaLabel.setText(f"Area: {data.get('strArea')}")
        self.instructionsLabel.setText(data.get('strInstructions'))

    def __parseIngredients(self, data) -> list[tuple[str, str]]:
        ingredients: list[tuple[str, str]] = []
        for i in range(1, 21):
            ingredients.append((data.get(f"strIngredient{i}"), data.get(f"strMeasure{i}")))

        def removeBadIngredients(ingredient: tuple[str, str]):
            if ingredient[0] == "" or ingredient[0] is None:
                return False

            return True

        ingredients = list(filter(removeBadIngredients, ingredients))
        return ingredients


class MealIngredientsWidget(QWidget):
    def __init__(self, ingredients: list[tuple[str, str]], parent: Optional[QWidget] = None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        for ingredient in ingredients:
            label = QLabel(f"- {ingredient[0]}: {ingredient[1]}")
            layout.addWidget(label)
