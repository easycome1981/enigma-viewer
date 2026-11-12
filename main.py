import threading
import time
import requests
from requests.auth import HTTPBasicAuth
from io import BytesIO
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.graphics import PushMatrix, PopMatrix, Scale, Translate

class EnigmaConfigScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20

        app = App.get_running_app()

        self.add_widget(Label(text="Configurare Enigma2 Kiosk", font_size=24, size_hint_y=None, height=50))

        self.ip_input = TextInput(text=app.ENIGMA2_IP, hint_text="IP Enigma2", multiline=False, size_hint_y=None, height=40)
        self.port_input = TextInput(text=str(app.PORT), hint_text="Port", multiline=False, size_hint_y=None, height=40)
        self.user_input = TextInput(text=app.USER, hint_text="Utilizator", multiline=False, size_hint_y=None, height=40)
        self.pass_input = TextInput(text=app.PASSWORD, hint_text="Parolă", password=True, multiline=False, size_hint_y=None, height=40)

        self.add_widget(Label(text="Adresă IP receptor:", size_hint_y=None, height=20))
        self.add_widget(self.ip_input)
        self.add_widget(Label(text="Port:", size_hint_y=None, height=20))
        self.add_widget(self.port_input)
        self.add_widget(Label(text="Utilizator:", size_hint_y=None, height=20))
        self.add_widget(self.user_input)
        self.add_widget(Label(text="Parolă:", size_hint_y=None, height=20))
        self.add_widget(self.pass_input)

        save_btn = Button(text="Salvează și Pornește", size_hint_y=None, height=60, background_color=(0, 0.7, 0, 1))
        save_btn.bind(on_press=self.save_config)
        self.add_widget(save_btn)

    def save_config(self, instance):
        app = App.get_running_app()
        app.ENIGMA2_IP = self.ip_input.text
        app.PORT = int(self.port_input.text)
        app.USER = self.user_input.text
        app.PASSWORD = self.pass_input.text
        app.start_streaming()

class EnigmaDirectApp(App):
    ENIGMA2_IP = "192.168.1.170"
    PORT = 7149
    USER = "root"
    PASSWORD = "12ony34"

    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        self.root_layout = FloatLayout()
        self.config_screen = EnigmaConfigScreen()
        self.root_layout.add_widget(self.config_screen)
        return self.root_layout

    def start_streaming(self):
        self.root_layout.clear_widgets()

        with self.root_layout.canvas.before:
            PushMatrix()
            Translate(Window.width / 2, Window.height / 2, 0)
            Scale(-1, 1, 1)
            Translate(-Window.width / 2, -Window.height / 2, 0)
        with self.root_layout.canvas.after:
            PopMatrix()

        self.img = KivyImage(allow_stretch=True, keep_ratio=True)
        self.root_layout.add_widget(self.img)
        
        self.lbl = Label(
            text="Se conectează la Enigma2...", 
            font_size=20, 
            color=(1, 1, 0, 1), 
            size_hint=(0.9, None), 
            height=100, 
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center',
            valign='middle'
        )
        self.lbl.bind(size=self.lbl.setter('text_size'))
        self.root_layout.add_widget(self.lbl)
        
        btn = Button(
            text="Setări", font_size=16, bold=True, 
            size_hint=(None, None), size=(80, 40), 
            pos_hint={'right': 0.98, 'top': 0.98}, 
            background_color=(0.8, 0, 0, 1)
        )
        btn.bind(on_press=self.return_to_config)
        self.root_layout.add_widget(btn)
        
        self.busy = False
        threading.Thread(target=self.download, daemon=True).start()
        Clock.schedule_interval(self.tick, 3.0)

    def return_to_config(self, instance):
        Clock.unschedule(self.tick)
        self.root_layout.clear_widgets()
        self.root_layout.canvas.before.clear()
        self.root_layout.canvas.after.clear()
        self.config_screen = EnigmaConfigScreen()
        self.root_layout.add_widget(self.config_screen)

    def tick(self, dt):
        if not self.busy:
            threading.Thread(target=self.download, daemon=True).start()

    def download(self):
        self.busy = True
        try:
            url = f"http://{self.ENIGMA2_IP}:{self.PORT}/lcd4linux/dpf2.jpg?{int(time.time()*1000)}"
            response = requests.get(url, auth=HTTPBasicAuth(self.USER, self.PASSWORD), timeout=5)
            
            if response.status_code == 200:
                from PIL import Image as PILImage
                img = PILImage.open(BytesIO(response.content)).convert("RGBA")
                data = img.tobytes()
                size = img.size
                Clock.schedule_once(lambda dt: self.update(data, size), 0)
            else:
                err_msg = f"Eroare HTTP {response.status_code}"
                Clock.schedule_once(lambda dt: setattr(self.lbl, 'text', err_msg), 0)
        except Exception as e:
            err_msg = "Eroare rețea / Receptor inaccesibil"
            Clock.schedule_once(lambda dt: setattr(self.lbl, 'text', err_msg), 0)
        finally:
            self.busy = False

    def update(self, data, size):
        try:
            tex = Texture.create(size=size, colorfmt='rgba')
            tex.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
            self.img.texture = tex
            self.lbl.text = ""
        except Exception as ex:
            self.lbl.text = f"Eroare redare: {str(ex)}"

if __name__ == '__main__':
    EnigmaDirectApp().run()
