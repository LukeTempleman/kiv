from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label

# Import pages from pages.py
from pages import PageTwo, PageThree, FormPage
from pageOne import PageOne
from loginScreen import LoginScreen

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (400, 200)
        self.add_widget(Image(source='images/logo1.png', size_hint=(1, 1)))
        self.splash_time = 7  # 5 seconds
        Clock.schedule_interval(self.update_splash_screen, 1)

    def update_splash_screen(self, dt):
        self.splash_time -= 1
        if self.splash_time <= 0:
            Clock.unschedule(self.update_splash_screen)
            self.manager.current = 'login_screen'  # Switch to PageOne after splash

class Dashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Set the main background to white
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Header layout with white background
        header = BoxLayout(orientation='horizontal', size_hint_y=0.1, padding=1, spacing=1)
        with header.canvas.before:
            Color(1, 1, 1, 1)  
            self.header_rect = Rectangle(size=header.size, pos=header.pos)
            header.bind(size=self._update_header_rect, pos=self._update_header_rect)

        logo = Image(source='images/logo1.png', size_hint=(1, 1))  # Logo size
        header.add_widget(logo)

        header_right = BoxLayout(orientation='horizontal', size_hint=(0.8, 1), spacing=1)
    
        off_btn = Button(
            text='Off',
            size_hint=(0.1, 1),
            font_size=20,
            color=(1, 1, 1 , 1),  # Text color
            background_color=(0.57, 2, 6.5, 1) # Background color
        )
        off_btn.bind(on_release=self.stop_app)
        header_right.add_widget(off_btn)

        header.add_widget(header_right)
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(SplashScreen(name='splash_screen'))
        self.screen_manager.add_widget(PageOne(name='page_one'))
        self.screen_manager.add_widget(PageTwo(name='page_two'))
        self.screen_manager.add_widget(PageThree(name='page_three'))
        self.screen_manager.add_widget(FormPage(name='page_four'))
        self.screen_manager.add_widget(LoginScreen(name='login_screen'))

        side_menu = BoxLayout(orientation='vertical', size_hint_x=0.2, padding=0, spacing=0)
        side_menu_buttons = [
            #('page_one', 'Robot'),
            ('page_two', 'Help'),
            ('page_three', 'Settings'),
            ('page_four', 'Form'),
        ]

        btnBegin = Button(text='Robot',
                          size_hint=(1, 0.2),
                          background_color=(0.57, 2, 6.5, 1),
                          on_release=self.callBegin)
        side_menu.add_widget(btnBegin)

        for page, text in side_menu_buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.2),
                background_color=(0.57, 2, 6.5, 1),
                on_release=lambda btn, page = page: self.switch_page(page)
            )
            side_menu.add_widget(btn)




        main_layout = BoxLayout(orientation='horizontal', size_hint_y=0.8)
        main_layout.add_widget(side_menu)
        main_layout.add_widget(self.screen_manager)

        self.add_widget(header)
        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def callBegin(self, instance):
        self.screen_manager.current = 'login_screen'

    def _update_header_rect(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size

    def switch_page(self, page_name):
        self.screen_manager.current = page_name

    def stop_app(self, *args):
        App.get_running_app().stop()



class DashboardApp(App):
    def build(self):
        return Dashboard()

if __name__ == '__main__':
    DashboardApp().run()
