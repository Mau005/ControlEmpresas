from kivy.lang import Builder

from kivymd.app import MDApp

screen = '''
Screen: 

    MDFloatingActionButtonSpeedDial:
        on_release_stack_button:app.callback
        data:app.data
        rotation_root_button:True
        hint_animation:True
        bg_hint_color: app.theme_cls.primary_light
'''


class Wolf(MDApp):
    data = {
        "help-rhombus": "Help",
        'triangle': 'Setting',
        'key': 'Register', }

    def callback(self, instance):
        if instance.icon == 'help-rhombus':
            print('Callback self.help-rhombus()')
        elif instance.icon == 'key':
            print('Callback self.key()')
        elif instance.icon == 'triangle':
            print('Callback self.triangles()')

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Green'
        screen_r = Builder.load_string(screen)
        return screen_r

Wolf().run()