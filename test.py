from kivymd.app import MDApp
from kivy.lang import Builder

Builder.load_file("kvlengs/root.kv")


class MyApp(MDApp):
    def build(self):
        return 

if __name__=="__main__":
    MyApp().run()