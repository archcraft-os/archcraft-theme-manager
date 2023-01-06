#!/usr/bin/python3
from kivy.config import Config
Config.set("graphics", "height", "650")
Config.set("graphics", "width", "380")
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
        self.openbox_theme_dir = "/home/{}/.config/openbox-themes/themes/".format(self.name_linux)
        self.openbox_theme_file = "/home/{}/.config/openbox-themes/themes/.current".format(self.name_linux)
        self.bspwm_theme_dir = "/home/{}/.config/bspwm-themes/themes/".format(self.name_linux)
        self.bspwm_theme_file = "/home/{}/.config/bspwm-themes/themes/.current".format(self.name_linux)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        self.MainUI = Builder.load_file("main.kv")
        self.InstallView = Builder.load_file("modal_views/install_theme.kv")
        from kivy.core.window import Window
        Window.size = [380,650]
        return self.MainUI

    def on_start(self):
        self.load_local_themes()
        self.load_popular()
        self.load_online()

    def refresh(self,*largs):
        self.on_start()
        Clock.schedule_once(lambda arg: self.root.ids.refresh_layout.refresh_done(),2)

    def load_popular(self):
        if len(self.root.ids.online_theme_top.children) > 4:
            self.root.ids.online_theme_top.clear_widgets()
        for theme in self.themes["Popular"].keys():
            Widget = ThemeViewOnline()
            Widget.source = self.themes["Popular"][theme]["thumbnail"]
            Widget.text = "{} by {}".format(theme,self.themes["Popular"][theme]["maker"])
            self.root.ids.online_theme_top.add_widget(Widget)

    def load_online(self):
        if len(self.root.ids.online_theme_lower.children) > 0:
            for child in self.root.ids.online_theme_lower.children:
                if len(self.root.ids.online_theme_lower.children) > 4:
                    self.root.ids.online_theme_lower.remove_widget(child)
        for theme in self.themes["Online"].keys():
            Widget = ThemeViewOnline()
            Widget.source = self.themes["Online"][theme]["thumbnail"]
            Widget.text = "{} by {}".format(theme,self.themes["Online"][theme]["maker"])
            self.root.ids.online_theme_lower.add_widget(Widget)

    def load_local_themes(self,*args):
        Animation(opacity=0,d=0.2).start(self.root.ids.local_themes)
        Clock.schedule_once(self.add_openbox_local_theme_widget,0.3)
        Clock.schedule_once(lambda arg : Animation(opacity=1,d=0.2).start(self.root.ids.local_themes),0.4)

    def add_openbox_local_theme_widget(self,arg):
        self.root.ids.local_themes.clear_widgets()
        all_themes = self.get_all_openbox_themes()
        current_theme = self.get_current_openbox_theme()
        all_themes.remove(current_theme)
        CurrentWidget = ThemeView()
        if os.path.isfile("./default_previews/{}.png".format(current_theme)):
            CurrentWidget.source = "./default_previews/{}.png".format(current_theme)
        else:
            self.openbox_theme_dir+f"/{current_theme}/preview.png"
        CurrentWidget.text = current_theme.capitalize()
        CurrentWidget.children[0].style = "outlined"
        CurrentWidget.children[0].line_color = self.theme_cls.accent_light
        CurrentWidget.children[0].line_width = dp(2)
        CurrentWidget.ids.is_current.opacity = 1
        self.root.ids.local_themes.add_widget(CurrentWidget)
        self.root.ids.openbox_scrollview.scroll_to(CurrentWidget)

        for theme in all_themes:
            TestWidget = ThemeView()
            if os.path.isfile("./default_previews/{}.png".format(theme)):
                TestWidget.source = "./default_previews/{}.png".format(theme) 
            else:
                TestWidget.source = self.openbox_theme_dir+f"/{theme}/preview.png"
            TestWidget.text = theme.capitalize()
            self.root.ids.local_themes.add_widget(TestWidget)

    def open_theme_installer(self,root):
        self.InstallView.ids.theme_name.text = root.text.split(" by ")[0]
        self.InstallView.ids.dev_name.text = root.text.split(" by ")[-1]
        self.InstallView.open() 

    def apply_theme_openbox(self,theme):
        if os.path.exists(self.openbox_theme_file[:-9]+f"/{theme}/apply.sh"):
            _thread.start_new_thread(lambda x,y: os.system(which("bash")+" "+self.openbox_theme_dir+f"/{theme}/apply.sh &"),("",""))
            Clock.schedule_once(self.load_local_themes)

    def get_current_openbox_theme(self) -> str:
        if os.path.isfile(self.openbox_theme_file):
            with open(self.openbox_theme_file,"r") as file:
                self.current_theme = file.read().split("\n")[0]
                file.close()
            return self.current_theme
        else:
            raise FileNotFoundError("It does'nt seems you have openbox-themes installed?")

    def set_current_openbox_theme(self,theme:str) -> None:
        if os.path.isfile(self.openbox_theme_file):
            with open(self.openbox_theme_file,"w") as file:
                file.write(theme)
                file.close()
            return theme
        else:
            raise FileNotFoundError("It does'nt seems you have openbox-themes installed?")

    def get_all_openbox_themes(self):
        if os.path.isdir("/".join(self.openbox_theme_file.split("/")[:-1])):
            files = os.listdir("/".join(self.openbox_theme_file.split("/")[:-1]))
            folders = [] 
            for file in files:
                if os.path.isdir(self.openbox_theme_dir+file):
                    folders.append(file)
        return folders


ThemeManager().run()
