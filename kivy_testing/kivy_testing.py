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

#
# import kivy
# kivy.require('1.9.0')
#
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.properties import ObjectProperty
# from kivy.uix.listview import ListItemButton
#
# class StudentListButton(ListItemButton):
#     pass
#
# class StudentDB(BoxLayout):
#     first_name_text_input = ObjectProperty()
#     last_name_text_input = ObjectProperty()
#     student_list = ObjectProperty()
#
#     def submit_student(self):
#         #Get the student name from textInputs
#         student_name = self.first_name_text_input.text + " " + self.last_name_text_input.text
#
#         #Add to ListView
#         self.student_list.adapter.data.extend([student_name])
#
#         #Reset ListView
#         self.student_list._trigger_reset_populate()
#
#         pass
#
#     def delete_student(self):
#         #If list item is selected:
#         if self.student_list.adapter.selection:
#             #Get the item's text
#             selection = self.student_list.adapter.selection[0].text
#
#             #Remove the matching item from ListView
#             self.student_list.adapter.data.remove(selection)
#
#             #Reset the ListView
#             self.student_list._trigger_reset_populate()
#
#
#     def replace_student(self):
#         #If list item is selected:
#         if self.student_list.adapter.selection:
#             # Get the item's text
#             selection = self.student_list.adapter.selection[0].text
#
#             # Remove the matching item from ListView
#             self.student_list.adapter.data.remove(selection)
#
#             # Get the student name from textInputs
#             student_name = self.first_name_text_input.text + " " + self.last_name_text_input.text
#
#             # Add to ListView
#             self.student_list.adapter.data.extend([student_name])
#
#             self.student_list._trigger_reset_populate()
#
# class StudentDBApp(App):
#     def build(self):
#         return StudentDB()
#
# dbApp = StudentDBApp()
# dbApp.run()
#
# import kivy
# kivy.require("1.9.0")
#
# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
#
# class SampleGridLayout(GridLayout):
#     pass
#
# class SampleApp(App):
#     def build(self):
#         return SampleGridLayout()
#
# sample_app = SampleApp()
# sample_app.run()
#

import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup

class CustomPopup(Popup):
    pass

class SampBoxLayout(BoxLayout):

    checkbox_is_active = ObjectProperty(False)

    def checkbox_18_clicked(self, instance, value):
        if value is True:
            print("Checkbox checked")

        else:
            print("Checkbox unchecked")

    blue = ObjectProperty(True)
    red = ObjectProperty(False)
    green = ObjectProperty(False)

    def switch_on(self, instancce, value):
        if value is True:
            print("Switch on")

        else:
            print("Switch off")

    def open_popup(self):
        the_popup = CustomPopup()
        the_popup.open()

    def spinner_clicked(self, value):
        print("Spinner Value: " + value)


class SampleApp(App):
    def build(self):
        Window.clearcolor = (1,1,1,1)
        return SampBoxLayout()

sample_app = SampleApp()
sample_app.run()