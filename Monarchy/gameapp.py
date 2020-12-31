import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from game import *
from itertools import compress


class Widget1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
    
        lay = QVBoxLayout(self)
        #personalMoneyButton = QPushButton("Personal Money: 10")
        #lay.addWidget(personalMoneyButton)
        treasuryMoneyButton = QPushButton("Treasury Money: " + str(game.treasury["money"]))
        

        lay.addWidget(treasuryMoneyButton)

class Widget2(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        self.widgetList2 = []
    
        first_lay = QHBoxLayout()
        newTaxLabel = QLabel("Raise a new Tax:")
        first_lay.addWidget(newTaxLabel)
        
        second_lay = QVBoxLayout()
        keys = game.people[0].attributes.keys()
        for key in keys:
            values = game.returnPeopleStats(key,"unique")
            second_lay.addWidget(QLabel("{}".format(key)))
            widgetVec = [key]
            for value in values:
                checkBox = QCheckBox("{}".format(value))
                checkBox.setChecked(True)
                widgetVec.append(checkBox)
                second_lay.addWidget(checkBox)
            self.widgetList2.append(widgetVec)
        
        
        third_lay = QHBoxLayout()
        flatTaxLabel = QLabel("Flat Tax")
        flatTaxEdit = QLineEdit("0")
        third_lay.addWidget(flatTaxLabel)
        third_lay.addWidget(flatTaxEdit)
        
        fourth_lay = QHBoxLayout()
        incomeTaxLabel = QLabel("Income Tax")
        incomeTaxEdit = QLineEdit("0.00")
        fourth_lay.addWidget(incomeTaxLabel)
        fourth_lay.addWidget(incomeTaxEdit)
        
        fifth_lay = QHBoxLayout()
        taxNameLabel = QLabel("Tax Name")
        taxNameEdit = QLineEdit("Generic Tax")
        fifth_lay.addWidget(taxNameLabel)
        fifth_lay.addWidget(taxNameEdit)
        
        sixth_lay = QHBoxLayout()
        submitTaxButton = QPushButton("Submit Tax")
        sixth_lay.addWidget(submitTaxButton)
        
        
        lay.addLayout(first_lay)
        lay.addLayout(second_lay)
        lay.addLayout(third_lay)
        lay.addLayout(fourth_lay)
        lay.addLayout(fifth_lay)
        lay.addLayout(sixth_lay)
        
        submitTaxButton.clicked.connect(lambda: self.submitTax(taxNameEdit.text(),
                                                               flatTaxEdit.text(),
                                                               incomeTaxEdit.text()))
    
    def submitTax(self,tax_name,flat_tax,income_tax):
        subset_keys = []
        subset_values = []
        subset_conditions = []
        tax_resource = "money"
        tax_type = ["flat","prop"]
        tax_amount = [float(flat_tax),float(income_tax)]
        for vec in self.widgetList2:
            subset_key = vec[0]
            subset_value_widgets = vec[1:(len(vec))]
            subset_value_indices = [widget.isChecked() for widget in subset_value_widgets]
            subset_values_names = [widget.text() for widget in subset_value_widgets]
            subset_value = list(compress(subset_values_names, subset_value_indices))
            subset_condition = "="
            
            subset_keys.append(subset_key)
            subset_values.append(subset_value)
            subset_conditions.append(subset_condition)
        
        new_tax = Tax(subset_keys,subset_values,subset_conditions, tax_name, tax_resource, 
                      tax_type, tax_amount)
        game.taxes.append(new_tax)

        


class Widget3(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        all_person = game.people[0]
        combined_dict = all_person.returnCombinedDict()

        #fix
        for key in combined_dict.keys():
            newLayer = QHBoxLayout()
            newTitleLabel = QLabel(str(key))
            newLayer.addWidget(newTitleLabel)
            
            value_type = type(combined_dict[key])
            
            if value_type == str:
                operations_list = ['count']
                for operation in operations_list:
                    statistic = game.returnPeopleStats(key, operation)
                    newLabel = QLabel(str(statistic))
                    newLayer.addWidget(newLabel)
            elif value_type == int:
                operations_list = ['mean','sum']
                for operation in operations_list:
                    statistic = game.returnPeopleStats(key, operation)
                    newLabel = QLabel(str(statistic))
                    newLayer.addWidget(newLabel)
            
            lay.addLayout(newLayer)
            
        

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
    app = QApplication(sys.argv)
    game = Game()
    game.nextTick()
    w = stackedExample()
    w.show()
    sys.exit(app.exec_())
    
        # for i in range(4):
        #     lay.addWidget(QLineEdit("{}".format(i)))