from msilib.schema import Control
from kivymd.app import MDApp


class ControlEmpresas(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def build(self):
        return super().build()
    
if __name__ == "__main__":
    ControlEmpresas().run()