# pages.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

class PageTwo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.add_widget(Label(text="SOP Page", font_size=32, color=(0, 153/255, 1, 1),bold=True))
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        
class PageThree(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set the background color to white
        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)
                
        self.add_widget(Label(text="Config Page", font_size=32, color=(0, 153/255, 1, 1), bold=True))  # Text color black for contrast
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class FormPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        form_title = Label(
            text="Inspection Form",
            font_size=35,
            color=(0, 153/255, 1, 1), 
            bold=True,
        )
        layout.add_widget(form_title)
        
        self.responses = {}
        self.create_form(layout)
        self.add_widget(layout)

    def create_form(self, layout):
        questions = [
            ("Did you visually inspect the bed for any visible biohazards (blood, vomit, etc.)?", ["Yes", "No"]),
            ("If you answered yes to question 1, did you remove and dispose of the biohazards properly according to infection control protocols?", ["Yes", "No"]),
            ("Did you remove all linens and personal belongings from the bed?", ["Yes", "No"]),
            ("Did you ensure the entire bed surface is unobstructed for the robot's operation?", ["Yes", "No"]),
        ]

        for index, (question_text, options) in enumerate(questions):
            question_label = Label(text=question_text, font_size=20, color=(0, 153/255, 1, 1))
            question_dropdown = DropDown()
            question_button = Button(text='Select', size_hint_y=None, height=44, font_size=25, background_color=(0, 153/255, 1, 1))
            question_button.bind(on_release=question_dropdown.open)
            question_dropdown.bind(on_select=lambda instance, x, index=index: self.update_response(x, index))
            
            for option in options:
                btn = Button(text=option, size_hint_y=None, height=44, background_color=(0, 153/255, 1, 1),)
                btn.bind(on_release=lambda btn: question_dropdown.select(btn.text))
                question_dropdown.add_widget(btn)
                
            layout.add_widget(question_label)
            layout.add_widget(question_button)

        submit_button = Button(text="Submit", size_hint=(None, None), size=(100, 50))
        submit_button.bind(on_release=self.validate_and_submit_form)
        layout.add_widget(submit_button)

    def update_response(self, selected_option, question_index):
        self.responses[question_index] = selected_option

    def validate_and_submit_form(self, instance):
        if len(self.responses) < 4:
            self.show_error_popup("Please answer all questions.")
            return
        
        valid = True
        for response in self.responses.values():
            if response == "No":
                valid = False
                break
        
        if not valid:
            self.show_error_popup("Please inspect the room accordingly.")
        else:
            print("Form submitted!")
            # Handle form submission logic here

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        error_message = Label(text=message, font_size=14)
        content.add_widget(error_message)
        
        close_button = Button(text="Close", size_hint_y=None, height=50)
        close_button.bind(on_release=lambda x: self.popup.dismiss())
        content.add_widget(close_button)
        
        self.popup = Popup(title="Validation Required", content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()