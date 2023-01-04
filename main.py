#!/usr/bin/python3

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.m_cardtextfield import M_CardTextField
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.loader import Loader
from shutil import which
import json
import os
import _thread

Loader.loading_image = "logo.gif"

class ThemeView(MDAnchorLayout):
    pass

class ThemeViewOnline(MDAnchorLayout):
    pass


class ThemeManager(MDApp):

    bold_font = "./fonts/Poppins-Bold.ttf"
    regular_font = "./fonts/Poppins-Regular.ttf"
    light_font = "./fonts/Poppins-Light.ttf"
    medium_font = "./fonts/Poppins-Medium.ttf"
    inbuit_themes = ['adaptive', 'beach', 'default', 'easy', 'forest', 'hack', 'manhattan', 'slime', 'spark', 'wave']
    themes = json.load(open("themes.json","r"))
    icon = "logo.png"
    title = "Archcraft Theme Manager"

    def build(self):
        self.name_linux = os.popen("whoami").read()[:-1]
        self.current_theme_file = "/home/{}/.config/openbox-themes/themes/.current".format(self.name_linux)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        self.MainUI = Builder.load_file("main.kv")
        from kivy.core.window import Window
        Window.size = [400,650]
        return self.MainUI

    def on_start(self):
        self.load_local_themes()
        self.load_popular()
        self.load_online()

    def load_popular(self):
        for theme in self.themes["Popular"].keys():
            Widget = ThemeViewOnline()
            Widget.source = self.themes["Popular"][theme]["thumbnail"]
            Widget.text = "{} by {}".format(theme,self.themes["Popular"][theme]["maker"])
            self.root.ids.online_theme_top.add_widget(Widget)

    def load_online(self):
        for theme in self.themes["Online"].keys():
            Widget = ThemeViewOnline()
            Widget.source = self.themes["Online"][theme]["thumbnail"]
            Widget.text = "{} by {}".format(theme,self.themes["Online"][theme]["maker"])
            self.root.ids.online_theme_lower.add_widget(Widget)

    def load_local_themes(self,*args):
        Animation(opacity=0,d=0.2).start(self.root.ids.local_themes)
        Clock.schedule_once(self.add_local_theme_widget,0.3)
        Clock.schedule_once(lambda arg : Animation(opacity=1,d=0.2).start(self.root.ids.local_themes),0.4)

    def add_local_theme_widget(self,arg):
        self.root.ids.local_themes.clear_widgets()
        all_themes = self.get_all_themes()
        current_theme = self.get_current_theme()
        all_themes.remove(current_theme)
        CurrentWidget = ThemeView()
        if os.path.isfile("./default_previews/{}.png".format(current_theme)):
            CurrentWidget.source = "./default_previews/{}.png".format(current_theme)
        else:
            self.current_theme_file[:-9]+f"/{current_theme}/preview.png"
        CurrentWidget.text = current_theme.capitalize()
        CurrentWidget.children[0].style = "outlined"
        CurrentWidget.children[0].line_color = self.theme_cls.accent_light
        CurrentWidget.children[0].line_width = dp(2)
        CurrentWidget.ids.is_current.opacity = 1
        self.root.ids.local_themes.add_widget(CurrentWidget)

        for theme in all_themes:
            TestWidget = ThemeView()
            if os.path.isfile("./default_previews/{}.png".format(theme)):
                TestWidget.source = "./default_previews/{}.png".format(theme) 
            else:
                TestWidget.source = self.current_theme_file[:-9]+f"/{theme}/preview.png"
            TestWidget.text = theme.capitalize()
            self.root.ids.local_themes.add_widget(TestWidget)

    def apply_theme(self,theme):
        if os.path.exists(self.current_theme_file[:-9]+f"/{theme}/apply.sh"):
            _thread.start_new_thread(lambda x,y: os.system(which("bash")+" "+self.current_theme_file[:-8]+f"/{theme}/apply.sh &"),("",""))
            Clock.schedule_once(self.load_local_themes)

    def get_current_theme(self) -> str:
        if os.path.isfile(self.current_theme_file):
            with open(self.current_theme_file,"r") as file:
                self.current_theme = file.read().split("\n")[0]
                file.close()
            return self.current_theme
        else:
            raise FileNotFoundError("It does'nt seems you have openbox-themes installed?")

    def set_current_theme(self,theme:str) -> None:
        if os.path.isfile(self.current_theme_file):
            with open(self.current_theme_file,"w") as file:
                file.write(theme)
                file.close()
            return theme
        else:
            raise FileNotFoundError("It does'nt seems you have openbox-themes installed?")

    def get_all_themes(self):
        if os.path.isdir("/".join(self.current_theme_file.split("/")[:-1])):
            return os.listdir("/".join(self.current_theme_file.split("/")[:-1]))[:-4]


ThemeManager().run()
