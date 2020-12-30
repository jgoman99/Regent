import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Widget1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
    
        lay = QVBoxLayout(self)
        personalMoneyButton = QPushButton("Personal Money: 10")
        treasuryMoneyButton = QPushButton("Treasury Money: 666")
        
        lay.addWidget(personalMoneyButton)
        lay.addWidget(treasuryMoneyButton)

class Widget2(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.lay = QVBoxLayout(self)
        
        self.pollTaxLabel = QLabel("Poll Tax (%)")
        self.pollTaxEdit = QLineEdit("0")
        self.pollTaxSlider =  QSlider(Qt.Horizontal)
        self.pollTaxSlider.setMinimum(0)
        self.pollTaxSlider.setMaximum(100)
        self.pollTaxSlider.setValue(20)
        self.pollTaxSlider.setTickPosition(QSlider.TicksBelow)
        self.pollTaxSlider.setTickInterval(5)
        
        self.oneLay = QHBoxLayout()
        self.oneLay.addWidget(self.pollTaxLabel)
        self.oneLay.addWidget(self.pollTaxEdit)
        self.lay.addLayout(self.oneLay)
        self.lay.addWidget(self.pollTaxSlider)
        
        self.pollTaxSlider.valueChanged.connect(self.valuechange)
    
    def valuechange(self):
        value = self.pollTaxSlider.value()
        self.pollTaxEdit.setText(str(value))
        
        


class Widget3(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        for i in range(4):
            lay.addWidget(QRadioButton("{}".format(i)))

class stackedExample(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        self.Stack = QStackedWidget()
        self.Stack.addWidget(Widget1())
        self.Stack.addWidget(Widget2())
        self.Stack.addWidget(Widget3())

        btnNext = QPushButton("Next")
        btnNext.clicked.connect(self.onNext)
        btnPrevious = QPushButton("Previous")
        btnPrevious.clicked.connect(self.onPrevious)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(btnPrevious)
        btnLayout.addWidget(btnNext)

        lay.addWidget(self.Stack)
        lay.addLayout(btnLayout)

    def onNext(self):
        self.Stack.setCurrentIndex((self.Stack.currentIndex()+1) % 3)

    def onPrevious(self):
        self.Stack.setCurrentIndex((self.Stack.currentIndex()-1) % 3)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = stackedExample()
    w.show()
    sys.exit(app.exec_())
    
        # for i in range(4):
        #     lay.addWidget(QLineEdit("{}".format(i)))