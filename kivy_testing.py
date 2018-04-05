# SRC: https://www.youtube.com/watch?v=6yMHHC36tT0&t=635s
# import kivy
#
# kivy.require('1.9.0')
#
# from kivy.app import App
# from kivy.uix.widget import Widget
#
#
# class CustomWidget(Widget):
#     pass
#
#
# class CustomWidgetApp(App):
#
#     def build(self):
#         return CustomWidget()
#
#
# customWidget = CustomWidgetApp()
#
# customWidget.run()
#
# import kivy
#
# kivy.require('1.9.0')
#
# from kivy.app import App
# from kivy.uix.floatlayout import FloatLayout
#
#
# # A Float layout positions and sizes objects as a percentage
# # of the window size
#
# class FloatingApp(App):
#
#     def build(self):
#         return FloatLayout()
#
#
# flApp = FloatingApp()
#
# flApp.run()

# import kivy
# kivy.require('1.9.0')
#
# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
#
# class GridApp(App):
#
#     def build(self):
#         return GridLayout()
#
# grApp = GridApp()
# grApp.run()

# import kivy
# kivy.require('1.9.0')
#
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
#
# class BoxApp(App):
#
#     def build(self):
#         return BoxLayout()
#
# bxApp = BoxApp()
# bxApp.run()

# import kivy
# kivy.require('1.9.0')
#
# from kivy.app import App
# from kivy.uix.stacklayout import StackLayout
#
# class StackApp(App):
#
#     def build(self):
#         return StackLayout()
#
# stckApp = StackApp()
# stckApp.run()
#
# import kivy
# kivy.require('1.9.0')
# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
#
# class CalcGridLayout(GridLayout):
#
#     def calculate(self, calculation):
#         if calculation:
#             try:
#                 self.display.text = str(eval(calculation))
#             except Exception:
#                 self.display.text = "ERR"
#
# class CalculatorApp(App):
#     def build(self):
#         return CalcGridLayout()
#
# calcApp = CalculatorApp()
# calcApp.run()
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton

class StudentListButton(ListItemButton):
    pass

class StudentDB(BoxLayout):
    first_name_text_input = ObjectProperty()
    last_name_text_input = ObjectProperty()
    student_list = ObjectProperty()

    def submit_students(self):
        pass

    def delete_student(self):
        pass

    def replace_stuent(self):
        pass

class StudentDBApp(App):
    def build(self):
        return StudentDB()

dbApp = StudentDBApp()
dbApp.run()


