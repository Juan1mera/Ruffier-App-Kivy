from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from seconds import Seconds
from functions import *

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(
            text='Test de Ruffier',
            size_hint=(1, 0.2),
            font_size='24sp'
        )
        
        form = GridLayout(cols=2, spacing=40, size_hint=(1, 0.03))
        
        form.add_widget(Label(text='Nombre:'))
        self.name_input = TextInput(multiline=False)
        form.add_widget(self.name_input)
        
        form.add_widget(Label(text='Edad:'))
        self.age_input = TextInput(multiline=False, input_filter='int')
        form.add_widget(self.age_input)
        
        next_button = Button(
            text='Continuar',
            size_hint=(1, 0.02),
            on_press=self.next_screen,
        )
        
        layout.add_widget(title)
        layout.add_widget(form)
        layout.add_widget(next_button)
        
        self.add_widget(layout)
    
    def next_screen(self, instance):
        if self.name_input.text and self.age_input.text:
            self.manager.get_screen('pulse1').age = int(self.age_input.text)
            self.manager.current = 'pulse1'

class Pulse1Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.age = 0
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        instructions = Label(
            text='Mide tu pulso en reposo durante 15 segundos\nCuenta las pulsaciones',
            size_hint=(1, 0.3),
            halign='center'
        )
        
        self.timer = Seconds(
            size_hint=(1, 0.15),
            font_size='30sp'
        )
        
        start_button = Button(
            text='Comenzar medición',
            size_hint=(1, 0.15),
            on_press=self.start_timer
        )
        
        form = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        form.add_widget(Label(text='Número de pulsaciones:'))
        self.pulse_input = TextInput(
            multiline=False,
            input_filter='int',
            size_hint=(1, None),
            height='40dp',
            disabled=True
        )
        form.add_widget(self.pulse_input)
        
        self.next_button = Button(
            text='Siguiente',
            size_hint=(1, 0.2),
            on_press=self.next_screen,
            disabled=True
        )
        
        layout.add_widget(instructions)
        layout.add_widget(self.timer)
        layout.add_widget(start_button)
        layout.add_widget(form)
        layout.add_widget(self.next_button)
        
        self.add_widget(layout)

    def start_timer(self, instance):
        def on_finish():
            self.pulse_input.disabled = False
            self.next_button.disabled = False
            instance.disabled = False
            
        self.pulse_input.disabled = True
        self.next_button.disabled = True
        instance.disabled = True
        self.timer.start(15, on_finish)
    
    def next_screen(self, instance):
        if self.pulse_input.text:
            pulse_value = int(self.pulse_input.text)
            self.manager.get_screen('pulse2').p1 = pulse_value
            self.manager.get_screen('pulse2').age = self.age
            self.manager.current = 'pulse2'

class Pulse2Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p1 = 0
        self.age = 0
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.instructions = Label(
            text='Haz 30 sentadillas en 45 segundos',
            size_hint=(1, 0.3),
            halign='center'
        )
        
        self.timer = Seconds(
            size_hint=(1, 0.15),
            font_size='30sp'
        )
        
        self.start_button = Button(
            text='Comenzar ejercicio',
            size_hint=(1, 0.15),
            on_press=self.start_exercise
        )
        
        form = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        form.add_widget(Label(text='Número de pulsaciones después del ejercicio:'))
        self.pulse_input = TextInput(
            multiline=False,
            input_filter='int',
            size_hint=(1, None),
            height='40dp',
            disabled=True
        )
        form.add_widget(self.pulse_input)
        
        self.next_button = Button(
            text='Siguiente',
            size_hint=(1, 0.2),
            on_press=self.next_screen,
            disabled=True
        )
        
        layout.add_widget(self.instructions)
        layout.add_widget(self.timer)
        layout.add_widget(self.start_button)
        layout.add_widget(form)
        layout.add_widget(self.next_button)
        
        self.add_widget(layout)

    def start_exercise(self, instance):
        def on_exercise_finish():
            self.instructions.text = 'Ahora mide tu pulso durante 15 segundos'
            self.start_button.disabled = True
            self.measure_pulse()
            
        self.start_button.disabled = True
        self.timer.start(45, on_exercise_finish)
        
    def measure_pulse(self):
        def on_pulse_finish():
            self.pulse_input.disabled = False
            self.next_button.disabled = False
            
        self.timer.start(15, on_pulse_finish)
    
    def next_screen(self, instance):
        if self.pulse_input.text:
            p2 = int(self.pulse_input.text)
            self.manager.get_screen('rest').p1 = self.p1
            self.manager.get_screen('rest').p2 = p2
            self.manager.get_screen('rest').age = self.age
            self.manager.current = 'rest'

class RestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p1 = 0
        self.p2 = 0
        self.age = 0
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.instructions = Label(
            text='Descansando durante 30 segundos',
            size_hint=(1, 0.3),
            halign='center',
            font_size='24sp'
        )
        
        self.timer = Seconds(
            size_hint=(1, 0.15),
            font_size='30sp'
        )
        
        # No necesitamos este botón ya que el temporizador iniciará automáticamente
        # Pero lo mantenemos oculto para no cambiar demasiado la estructura
        self.start_button = Button(
            text='Comenzar descanso',
            size_hint=(1, 0.15),
            on_press=self.start_timer,
            opacity=0,
            disabled=True
        )
        
        self.next_button = Button(
            text='Siguiente',
            size_hint=(1, 0.2),
            on_press=self.next_screen,
            disabled=True,
            opacity=0  # Oculto ya que pasaremos automáticamente
        )
        
        layout.add_widget(self.instructions)
        layout.add_widget(self.timer)
        layout.add_widget(self.start_button)
        layout.add_widget(self.next_button)
        
        self.add_widget(layout)
    
    def on_enter(self):
        # Inicia el temporizador automáticamente cuando se entra a esta pantalla
        self.start_timer(None)

    def start_timer(self, instance):
        def on_finish():
            self.next_screen(None)
            
        self.timer.start(30, on_finish)
    
    def next_screen(self, instance):
        self.manager.get_screen('pulse3').p1 = self.p1
        self.manager.get_screen('pulse3').p2 = self.p2
        self.manager.get_screen('pulse3').age = self.age
        self.manager.current = 'pulse3'

class Pulse3Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p1 = 0
        self.p2 = 0
        self.age = 0
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        instructions = Label(
            text='Mide tu pulso durante 15 segundos',
            size_hint=(1, 0.3),
            halign='center'
        )
        
        self.timer = Seconds(
            size_hint=(1, 0.15),
            font_size='30sp'
        )
        
        start_button = Button(
            text='Comenzar medición',
            size_hint=(1, 0.15),
            on_press=self.start_timer
        )
        
        form = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        form.add_widget(Label(text='Número de pulsaciones:'))
        self.pulse_input = TextInput(
            multiline=False,
            input_filter='int',
            size_hint=(1, None),
            height='40dp',
            disabled=True
        )
        form.add_widget(self.pulse_input)
        
        self.next_button = Button(
            text='Ver resultados',
            size_hint=(1, 0.2),
            on_press=self.show_results,
            disabled=True
        )
        
        layout.add_widget(instructions)
        layout.add_widget(self.timer)
        layout.add_widget(start_button)
        layout.add_widget(form)
        layout.add_widget(self.next_button)
        
        self.add_widget(layout)

    def start_timer(self, instance):
        def on_finish():
            self.pulse_input.disabled = False
            self.next_button.disabled = False
            instance.disabled = False
            
        self.pulse_input.disabled = True
        self.next_button.disabled = True
        instance.disabled = True
        self.timer.start(15, on_finish)
    
    def show_results(self, instance):
        if self.pulse_input.text:
            p3 = int(self.pulse_input.text)
            result = test(self.p1, self.p2, p3, self.age)
            self.manager.get_screen('results').result_text = result
            self.manager.current = 'results'

class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result_text = ""
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.result_label = Label(
            text='',
            size_hint=(1, 0.7),
            halign='center',
            valign='middle',
            text_size=(400, None)
        )
        
        restart_button = Button(
            text='Realizar nueva prueba',
            size_hint=(1, 0.3),
            on_press=self.restart_test
        )
        
        layout.add_widget(self.result_label)
        layout.add_widget(restart_button)
        
        self.add_widget(layout)
    
    def on_pre_enter(self):
        self.result_label.text = self.result_text
    
    def restart_test(self, instance):
        self.manager.current = 'welcome'
        self.manager.get_screen('welcome').name_input.text = ''
        self.manager.get_screen('welcome').age_input.text = ''
        self.manager.get_screen('pulse1').pulse_input.text = ''
        self.manager.get_screen('pulse2').pulse_input.text = ''
        self.manager.get_screen('pulse3').pulse_input.text = ''

class RuffierApp(App):
    def build(self):
        Window.size = (400, 700)
        
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(Pulse1Screen(name='pulse1'))
        sm.add_widget(Pulse2Screen(name='pulse2'))
        sm.add_widget(RestScreen(name='rest'))
        sm.add_widget(Pulse3Screen(name='pulse3'))
        sm.add_widget(ResultsScreen(name='results'))
        
        return sm

if __name__ == '__main__':
    RuffierApp().run()