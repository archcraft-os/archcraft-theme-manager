#!/usr/bin/python3
import kivy
from kivy.config import Config

Config.set("graphics", "height", "650")
Config.set("graphics", "width", "380")
Config.set("input", "%(name)s", "probesysfs,provider=hidinput")
Config.set("kivy", "exit_on_escape", "0")
Config.set("kivy", "pause_on_minimize", "0")

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.m_cardtextfield import M_CardTextField
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.tab import MDTabsBase
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.loader import Loader
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from shutil import which
from urllib.request import urlopen
import time
import json
import os
import _thread
import configparser


class ThemeView(MDAnchorLayout):
    pass


class ThemeViewOnline(MDAnchorLayout):
    pass


class Tab(MDFloatLayout, MDTabsBase):
    pass


class ThemeManager(MDApp):

    themes = json.load(open("../themes.json", "r"))
    icon = "logo.png"
    title = "Archcraft Theme Manager"

    def parse_settings(self) -> dict:
        config = configparser.ConfigParser()
        try:
            config.read(
                self.config_file if os.path.isfile(self.config_file) else "config.ini"
            )
        except Exception:
            kivy.logger.Logger.error(
                "archcraft-theme-manager : unable to read config file"
            )
            exit(1)
        return config["archcraft-theme-manager"]

    def settings_updater(self):
        while True:
            time.sleep(0.5)
            try:
                self.apply_settings()
            except Exception:
                pass

    def get_running_session(self):
        if os.system("pgrep -x openbox") == 0:
            return "openbox"

        elif os.system("pgrep -x bspwm") == 0:
            return "bspwm"

    def apply_settings(self):
        self.config = self.parse_settings()
        self.bold_font = self.config["bold_font"]
        self.regular_font = self.config["regular_font"]
        self.medium_font = self.config["medium_font"]
        self.theme_cls.theme_style = self.config["theme_style"]
        self.theme_cls.primary_palette = self.config["primary_palette"]
        self.theme_cls.accent_palette = self.config["accent_palette"]
        self.theme_cls.primary_hue = self.config["primary_hue"]
        self.theme_cls.accent_hue = self.config["accent_hue"]
        self.theme_cls.heme_style_switch_animation = self.config[
            "theme_style_switch_animation"
        ]
        self.theme_cls.theme_style_switch_animation_duration = float(
            self.config["theme_style_switch_animation_duration"]
        )
        self.theme_cls.custom_normal = (
            self.theme_cls.bg_normal
            if self.config["bg_normal"].lower() == "none"
            else self.config["bg_normal"]
        )
        self.theme_cls.custom_light = (
            self.theme_cls.bg_light
            if self.config["bg_light"].lower() == "none"
            else self.config["bg_light"]
        )
        self.theme_cls.custom_dark = (
            self.theme_cls.bg_light
            if self.config["bg_dark"].lower() == "none"
            else self.config["bg_dark"]
        )
        self.theme_cls.custom_darkest = (
            self.theme_cls.bg_light
            if self.config["bg_darkest"].lower() == "none"
            else self.config["bg_darkest"]
        )
        Loader.loading_image = (
            "./assets/loading.png"
            if self.config["loading_image"].lower() == "default"
            else self.config["loading_image"].lower()
        )

    def build(self):
        self.name_linux = os.popen("whoami").read()[:-1]
        self.openbox_theme_dir = "/home/{}/.config/openbox-themes/themes/".format(
            self.name_linux
        )
        self.openbox_theme_file = (
            "/home/{}/.config/openbox-themes/themes/.current".format(self.name_linux)
        )
        self.bspwm_theme_dir = "/home/{}/.config/bspwm/themes/".format(self.name_linux)
        self.bspwm_theme_file = "/home/{}/.config/bspwm/themes/.current".format(
            self.name_linux
        )
        self.config_file = "/home/{}/.config/archcraft-theme-manager/config.ini".format(
            self.name_linux
        )
        if os.path.isfile(self.config_file) == False:
            kivy.logger.Logger.warning(
                "archcraft-theme-manager : not found {}".format(self.config_file)
            )
            kivy.logger.Logger.warning(
                "archcraft-theme-manager : Reading default config file"
            )
        self.apply_settings()
        _thread.start_new_thread(self.settings_updater, ())
        self.theme_cls.material_style = "M3"
        self.MainUI = Builder.load_file("main.kv")
        self.InstallView = Builder.load_file("modal_views/install_theme.kv")
        self.DynamicView = Builder.load_file("modal_views/dynamic_view.kv")
        from kivy.core.window import Window

        Window.size = [380, 650]
        return self.MainUI

    def on_start(self):
        Clock.schedule_interval(
            self.load_themes_json, float(self.config["update_time"])
        )
        self.load_local_themes_bspwm()
        self.load_local_themes_openbox()
        self.load_popular()
        self.load_online()

    def refresh_offline_openbox(self, *largs):
        self.load_local_themes_openbox()
        Clock.schedule_once(
            lambda arg: self.root.ids.openbox_scrollview.refresh_done(), 2
        )

    def refresh_offline_bspwm(sef, *largs):
        self.load_local_themes_bspwm()
        Clock.schedule_once(
            lambda arg: self.root.ids.bspwm_scrollview.refresh_done(), 2
        )

    def refresh_online(self, *largs):
        self.load_popular()
        self.load_online()
        Clock.schedule_once(
            lambda arg: self.root.ids.refresh_layout_online.refresh_done(), 2
        )

    def space_widget(self, size_y):
        Widget = BoxLayout()
        Widget.size_hint = [None, None]
        Widget.size = [dp(50), size_y]
        return Widget

    def load_popular(self):
        if len(self.root.ids.online_theme_top.children) > 4:
            self.root.ids.online_theme_top.clear_widgets()
        for theme in self.themes["Popular"].keys():
            Widget = ThemeViewOnline()
            Widget.source = self.themes["Popular"][theme]["thumbnail"]
            Widget.text = "{} by {}".format(
                theme, self.themes["Popular"][theme]["maker"]
            )
            Widget.file_size = self.themes["Popular"][theme]["file_size"]
            Widget.download_url = self.themes["Popular"][theme]["downloadurl"]
            Widget.wm = self.themes["Popular"][theme]["wm"]
            if (
                theme.lower()
                in self.get_all_openbox_themes() + self.get_all_bspwm_themes()
            ):
                Widget.installed = True
            self.root.ids.online_theme_top.add_widget(Widget)

    def load_online(self):
        if len(self.root.ids.online_theme_lower.children) > 0:
            for child in self.root.ids.online_theme_lower.children:
                if len(self.root.ids.online_theme_lower.children) > 4:
                    self.root.ids.online_theme_lower.remove_widget(child)
        for theme in self.themes["Online"].keys():
            Widget = ThemeViewOnline()
            Widget.source = self.themes["Online"][theme]["thumbnail"]
            Widget.text = "{} by {}".format(
                theme, self.themes["Online"][theme]["maker"]
            )
            Widget.file_size = self.themes["Online"][theme]["file_size"]
            Widget.download_url = self.themes["Online"][theme]["downloadurl"]
            Widget.wm = self.themes["Online"][theme]["wm"]
            if (
                theme.lower()
                in self.get_all_openbox_themes() + self.get_all_bspwm_themes()
            ):
                Widget.installed = True
            self.root.ids.online_theme_lower.add_widget(Widget)

    def load_local_themes_openbox(self, *args):
        Animation(opacity=0, d=0.2).start(self.root.ids.local_themes)
        Clock.schedule_once(self.add_openbox_local_theme_widget, 0.5)
        Clock.schedule_once(
            lambda arg: Animation(opacity=1, d=0.2).start(self.root.ids.local_themes),
            0.8,
        )
        Clock.schedule_once(
            lambda arg: Animation(opacity=0, d=0.2).start(self.root.ids.load_label), 0.8
        )

    def load_local_themes_bspwm(self, *args):
        Animation(opacity=0, d=0.2).start(self.root.ids.local_themes_bspwm)
        Clock.schedule_once(self.add_bspwm_local_theme_widget, 0.5)
        Clock.schedule_once(
            lambda arg: Animation(opacity=1, d=0.2).start(
                self.root.ids.local_themes_bspwm
            ),
            0.8,
        )
        Clock.schedule_once(
            lambda arg: Animation(opacity=0, d=0.2).start(
                self.root.ids.load_label_bspwm
            ),
            0.8,
        )

    def add_openbox_local_theme_widget(self, arg):
        self.root.ids.local_themes.clear_widgets()
        all_themes = self.get_all_openbox_themes()
        current_theme = self.get_current_openbox_theme()
        all_themes.remove(current_theme)
        CurrentWidget = ThemeView()
        if os.path.isfile("./default_previews/{}_openbox.png".format(current_theme)):
            CurrentWidget.source = "./default_previews/{}_openbox.png".format(
                current_theme
            )
        else:
            CurrentWidget.source = (
                self.openbox_theme_dir + f"{current_theme}/preview.png"
            )
        CurrentWidget.text = current_theme.capitalize()
        CurrentWidget.children[0].style = "outlined"
        CurrentWidget.children[0].line_color = self.theme_cls.accent_color
        CurrentWidget.children[0].line_width = dp(2)
        CurrentWidget.ids.is_current.opacity = 1
        self.root.ids.local_themes.add_widget(self.space_widget(dp(30)))
        self.root.ids.local_themes.add_widget(CurrentWidget)
        self.root.ids.openbox_scrollview.scroll_to(
            self.root.ids.local_themes.children[-1]
        )

        for theme in all_themes:
            TestWidget = ThemeView()
            if os.path.isfile("./default_previews/{}_openbox.png".format(theme)):
                TestWidget.source = "./default_previews/{}_openbox.png".format(theme)
            else:
                TestWidget.source = self.openbox_theme_dir + f"{theme}/preview.png"
            TestWidget.text = theme.capitalize()
            self.root.ids.local_themes.add_widget(TestWidget)

    def add_bspwm_local_theme_widget(self, arg):
        self.root.ids.local_themes_bspwm.clear_widgets()
        all_themes = self.get_all_bspwm_themes()
        current_theme = self.get_current_bspwm_theme()
        all_themes.remove(current_theme)
        CurrentWidget = ThemeView()
        if os.path.isfile("./default_previews/{}_bspwm.png".format(current_theme)):
            CurrentWidget.source = "./default_previews/{}_bspwm.png".format(
                current_theme
            )
        else:
            CurrentWidget.source = self.bspwm_theme_dir + f"{current_theme}/preview.png"
        CurrentWidget.text = current_theme.capitalize()
        CurrentWidget.children[0].style = "outlined"
        CurrentWidget.children[0].line_color = self.theme_cls.accent_color
        CurrentWidget.children[0].line_width = dp(2)
        CurrentWidget.ids.is_current.opacity = 1
        CurrentWidget.type = "bspwm"
        self.root.ids.local_themes_bspwm.add_widget(self.space_widget(dp(30)))
        self.root.ids.local_themes_bspwm.add_widget(CurrentWidget)
        self.root.ids.bspwm_scrollview.scroll_to(
            self.root.ids.local_themes_bspwm.children[-1]
        )

        for theme in all_themes:
            TestWidget = ThemeView()
            if os.path.isfile("./default_previews/{}_bspwm.png".format(theme)):
                TestWidget.source = "./default_previews/{}_bspwm.png".format(theme)
            else:
                TestWidget.source = self.openbox_theme_dir + f"{theme}/preview.png"
            TestWidget.text = theme.capitalize()
            TestWidget.type = "bspwm"
            self.root.ids.local_themes_bspwm.add_widget(TestWidget)

    def open_theme_installer(self, root):
        self.InstallView.ids.theme_name.text = (
            f"[font={self.regular_font}]Name : [/font]" + root.text.split(" by ")[0]
        )
        self.InstallView.ids.dev_name.text = (
            f"[font={self.regular_font}]Creator : [/font]" + root.text.split(" by ")[-1]
        )
        self.InstallView.ids.file_size.text = (
            f"[font={self.regular_font}]Size : [/font]" + root.file_size
        )
        self.InstallView.ids.theme_wm.text = (
            f"[font={self.regular_font}]WM : [/font]" + root.wm
        )
        self.InstallView.ids.image.source = root.source
        self.InstallView.ids.install_button.url = root.download_url
        self.InstallView.ids.install_button.name = root.text.split(" by ")[0]
        self.InstallView.ids.install_button.text = (
            "Installed"
            if root.text.split(" by ")[0].lower()
            in self.get_all_bspwm_themes() + self.get_all_openbox_themes()
            else "Install"
        )
        self.InstallView.open()

    def open_search_box(self):
        Animation(
            pos_hint={
                "center_y": 0.38
                if self.root.ids.search_box.pos_hint["center_y"] == -1
                else -1
            },
            radius=[dp(20), dp(20), 0, 0]
            if self.root.ids.search_box.radius == [0] * 4
            else [0] * 4,
            d=0.3,
            t="in_out_cubic",
        ).start(self.root.ids.search_box)
        self.handle_search()

    def handle_search(self, text="", search=False):
        def add_icon_item(theme_name):
            self.root.ids.search_view.data.append(
                {
                    "viewclass": "ThemeViewOnline",
                    "text": theme_name
                    + " by "
                    + (
                        self.themes["Online"][theme_name]["maker"]
                        if theme_name in self.themes["Online"].keys()
                        else self.themes["Popular"][theme_name]["maker"]
                    ),
                    "size_hint": [1, None],
                    "size": [dp(50), dp(180)],
                    "source": self.themes["Online"][theme_name]["thumbnail"]
                    if theme_name in self.themes["Online"].keys()
                    else self.themes["Popular"][theme_name]["thumbnail"],
                    "installed": True
                    if theme_name.lower() in self.get_all_openbox_themes()
                    else False,
                    "file_size": self.themes["Online"][theme_name]["file_size"]
                    if theme_name in self.themes["Online"].keys()
                    else self.themes["Popular"][theme_name]["file_size"],
                    "download_url": self.themes["Online"][theme_name]["downloadurl"]
                    if theme_name in self.themes["Online"].keys()
                    else self.themes["Popular"][theme_name]["downloadurl"],
                    "wm": self.themes["Online"][theme_name]["wm"]
                    if theme_name in self.themes["Online"].keys()
                    else self.themes["Popular"][theme_name]["wm"],
                }
            )

        self.root.ids.search_view.data = []
        self.root.ids.search_view.data.append(
            {"viewclass": "MDLabel", "size_hint": [1, None], "size": [dp(10), dp(30)]}
        )
        if search:
            for theme in list(self.themes["Online"].keys()) + list(
                self.themes["Popular"].keys()
            ):
                if text.strip().lower() in theme.lower():
                    add_icon_item(theme)

        else:
            for theme in list(self.themes["Online"].keys()) + list(
                self.themes["Popular"].keys()
            ):
                add_icon_item(theme)

    def apply_theme_openbox(self, theme):
        if self.get_running_session() != "openbox":
            self.send_notification("Openbox not running")
            return

        self.root.ids.load_label.opacity = 1
        if os.path.exists(self.openbox_theme_file[:-9] + f"/{theme}/apply.sh"):
            _thread.start_new_thread(
                lambda x, y: os.system(
                    which("nohup")
                    + " "
                    + which("bash")
                    + " "
                    + self.openbox_theme_dir
                    + f"/{theme}/apply.sh"
                ),
                ("", ""),
            )
            Clock.schedule_once(self.load_local_themes_openbox)

    def apply_theme_bspwm(self, theme):
        if self.get_running_session() != "bspwm":
            self.send_notification("Bspwm not running")
            return
        self.root.ids.load_label_bspwm.opacity = 1
        if os.path.exists(self.bspwm_theme_file[:-9] + f"/{theme}/apply.sh"):
            _thread.start_new_thread(
                lambda x, y: os.system(
                    which("nohup")
                    + " "
                    + which("bash")
                    + " "
                    + self.bspwm_theme_dir
                    + f"/{theme}/apply.sh"
                ),
                ("", ""),
            )
            Clock.schedule_once(self.load_local_themes_bspwm)

    def get_current_openbox_theme(self) -> str:
        if os.path.isfile(self.openbox_theme_file):
            with open(self.openbox_theme_file, "r") as file:
                self.current_theme = file.read().split("\n")[0]
                file.close()
            return self.current_theme
        else:
            raise FileNotFoundError(
                "It does'nt seems you have openbox-themes installed?"
            )

    def get_current_bspwm_theme(self) -> str:
        if os.path.isfile(self.bspwm_theme_file):
            with open(self.bspwm_theme_file, "r") as file:
                self.current_theme = file.read().split("\n")[0]
                file.close()
            return self.current_theme
        else:
            raise FileNotFoundError("It does'nt seems you have bspwm-themes installed?")

    def set_current_openbox_theme(self, theme: str) -> None:
        if os.path.isfile(self.openbox_theme_file):
            with open(self.openbox_theme_file, "w") as file:
                file.write(theme)
                file.close()
            return theme
        else:
            raise FileNotFoundError(
                "It does'nt seems you have openbox-themes installed?"
            )

    def get_all_openbox_themes(self):
        if os.path.isdir("/".join(self.openbox_theme_file.split("/")[:-1])):
            files = os.listdir("/".join(self.openbox_theme_file.split("/")[:-1]))
            folders = []
            for file in files:
                if os.path.isdir(self.openbox_theme_dir + file):
                    folders.append(file)
        return folders

    def get_all_bspwm_themes(self):
        if os.path.isdir("/".join(self.bspwm_theme_file.split("/")[:-1])):
            files = os.listdir("/".join(self.bspwm_theme_file.split("/")[:-1]))
            folders = []
            for file in files:
                if os.path.isdir(self.bspwm_theme_dir + file):
                    folders.append(file)
        return folders

    def send_notification(self, text):
        def construct_bar(arg):
            bar = Snackbar(
                text=text,
                snackbar_x="10dp",
                snackbar_y="100dp",
                shadow_softness=20,
                size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
            )
            bar.font_name = self.regular_font
            bar.open()

        Clock.schedule_once(construct_bar)

    def download_file(self, url):
        self.set_value(self.DynamicView.ids.text_main, "Downloding ...")
        if os.path.isdir("/home/{}/.cache/atm".format(self.name_linux)) == False:
            os.system("mkdir ~/.cache/atm/")
        os.system("rm -rf ~/.cache/atm/*")  # clear previous files
        # This most common file name finding algorithm
        filename = "/home/{}/.cache/atm/{}".format(self.name_linux, url.split("/")[-1])
        if os.system(which("wget") + " " + url + " -O {}".format(filename)) == 0:
            _thread.start_new_thread(lambda x, y: self.install_file(filename), ("", ""))
        else:
            self.set_value(self.DynamicView.ids.text_main, "Download Failed")
            Clock.schedule_once(lambda x: self.DynamicView.dismiss(), 1)
            self.send_notification(
                "Theme installation failed {}".format(self.theme_name)
            )

    # the above and below functions are kinda mess
    # but they work as intended

    def install_file(self, filename):
        self.set_value(self.DynamicView.ids.text_main, "Installing ...")
        if (
            os.system(
                "cd {} && {} -xvf {} ".format(
                    "/".join(filename.split("/")[:-1]), which("tar"), filename
                )
            )
            != 0
        ):
            return
        for folder in os.listdir("/".join(filename.split("/")[:-1])):
            if os.path.isdir("/".join(filename.split("/")[:-1]) + "/" + folder):
                command = (
                    "cd {} && ".format(
                        "/".join(filename.split("/")[:-1]) + "/" + folder
                    )
                    + which("bash")
                    + " "
                    + "/".join(filename.split("/")[:-1])
                    + "/"
                    + folder
                    + "/install.sh"
                )
                if os.system(command) == 0:
                    preview = (
                        "/".join(filename.split("/")[:-1])
                        + "/"
                        + folder
                        + "/preview.png"
                    )
                    if os.path.isfile(preview):
                        os.system(
                            "mv {} {}".format(
                                preview,
                                self.openbox_theme_dir
                                + self.theme_name.lower()
                                + "/preview.png",
                            )
                        )
                self.set_value(self.DynamicView.ids.text_main, "Done!")
                Clock.schedule_once(lambda x: self.DynamicView.dismiss(), 1)

                self.send_notification(
                    "Theme installation success {}".format(self.theme_name)
                )
                return
        self.set_value(self.DynamicView.ids.text_main, "Failed")
        self.send_notification("Theme installation failed {}".format(self.theme_name))

    def set_value(self, key, value):
        def run(arg):
            key.text = value

        Clock.schedule_once(run)

    def install_theme(self, url, name):
        self.DynamicView.open()
        self.theme_name = name
        _thread.start_new_thread(lambda x, y: self.download_file(url), ("", ""))

    def load_themes_json(self, arg):
        try:
            response = urlopen(
                "https://raw.githubusercontent.com/archcraft-os/archcraft-theme-manager/main/themes.json"
            )
            # Below lines are not working idk why?
            # with open("../themes.json","w") as theme_file:
            #   text = response.read()
            #   theme_file.write(str(text))
            # file.close()
        except Exception:
            return


if which("wget") == None:
    raise FileNotFoundError("Wget is not installed on your system, install it")

if os.path.isfile("/etc/os-release"):
    with open("/etc/os-release", "r") as file:
        if file.read().split("\n")[0].split('="')[-1][:-1] != "Archcraft":
            raise OSError("System is not Archcraft")

ThemeManager().run()
