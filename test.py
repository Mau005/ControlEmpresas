from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog.dialog import MDDialog

KV = '''
MDFloatLayout:

    MDFlatButton:
        text: "ALERT DIALOG"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.show_alert_dialog()
'''


class CustomDialogBox(MDDialog):
    def __init__(self, **kwargs):
        self.title = 'Title'
        self.text = 'Text'
        self.auto_dismiss = False
        self.accept = MDFlatButton(text='Accept', on_release=self.custom_dismiss)
        self.cancel = MDFlatButton(text='Cancel', on_release=self.custom_dismiss)
        self.buttons = [self.accept, self.cancel]
        super().__init__(**kwargs)

    def custom_dismiss(self, *Args):
        self.dismiss()


class Example(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_string(KV)

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = CustomDialogBox()
        self.dialog.open()


Example().run()