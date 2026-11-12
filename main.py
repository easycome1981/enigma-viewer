from kivy.app import App
from kivy.uix.label import Label

class EnigmaApp(App):
    def build(self):
        return Label(text='Salut Enigma2!')

if __name__ == '__main__':
    EnigmaApp().run()
