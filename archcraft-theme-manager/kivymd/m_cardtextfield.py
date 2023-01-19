"""
M_CardTextField
"""
__all__ = ("M_CardTextField",)

from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    VariableListProperty,
    ColorProperty
)
from kivy.core.text import DEFAULT_FONT
from kivy.config import Config
from kivy.event import EventDispatcher

_is_desktop = False
if Config:
    _is_desktop = Config.getboolean('kivy', 'desktop')

Builder.load_string(
    """
# kv_start
<M_CardTextField>:
    adaptive_height: True
    md_bg_color: 1, 1, 1, 1
    MDCard:
        id: card
        ripple_behavior: root.card_ripples
        radius: root.radius
        padding: root.card_padding
        size_hint_y: None 
        height: self.minimum_height
        elevation: 0
        md_bg_color: root.md_bg_color
        on_release:
            root.dispatch("on_release")
        TextInput:
            id: textfield
            grow: True
            text: root.text
            initial_height: 0
            focus: root.focus
            hint_text: root.hint_text
            input_type: root.input_type
            multiline: root.multiline
            background_normal: root.text_field_background_normal
            background_active: root.text_field_background_active
            background_disabled_normal: root.background_disabled_normal
            cursor_color: root.cursor_color
            foreground_color: root.foreground_color
            disabled_foreground_color: root.disabled_foreground_color
            disabled: root.text_field_disabled
            input_filter: root.input_filter
            line_spacing: root.line_spacing
            allow_copy: root.allow_copy
            replace_crlf: root.replace_crlf
            auto_indent: root.auto_indent
            handle_image_middle: root.handle_image_middle
            handle_image_left: root.handle_image_left
            handle_image_right: root.handle_image_right
            write_tab: root.write_tab
            base_direction: root.base_direction
            font_family: root.font_family
            font_context: root.font_context
            font_size: root.font_size
            font_name: root.font_name
            selection_text: root.selection_text
            readonly: root.readonly
            text_validate_unfocus: root.text_validate_unfocus
            password: root.password
            password_mask: root.password_mask
            keyboard_suggestions: root.keyboard_suggestions
            cursor_blink: root.cursor_blink
            cursor_width: root.cursor_width
            line_height: root.line_height
            tab_width: root.tab_width
            text_field_padding: root.text_field_padding
            halign: root.halign
            scroll_x: root.scroll_x
            scroll_y: root.scroll_y
            selection_color: root.selection_color
            background_color: root.background_color
            hint_text_color: root.hint_text_color
            border: root.border
            use_bubble: root.use_bubble
            use_handles: root.use_handles
            suggestion_text: root.suggestion_text
            size_hint_y: None if root.grow_card else root.text_field_size_hint_y
            height: 
                (self.minimum_height if self.height < root.text_field_max_height else root.text_field_max_height)\
                if root.grow_card else\
                (root.text_field_height if root.text_field_height and (not root.text_field_size_hint_y)\
                else self.minimum_height)
                
            on_text:
                self.initial_height = self.height if self.grow else self.initial_height
                self.grow = False
                self.height = self.initial_height if self.text == "" else self.height
                
            on_text:
                root.dispatch("on_text")
                root.text = self.text
                
            on_text_validate:
                root.dispatch("on_text_validate")
                
            on_focus:
                root.dispatch("on_focus")
                
            on_triple_tap:
                root.dispatch("on_triple_tap")
                
            on_double_tap:
                root.dispatch("on_double_tap")
                
            on_quad_touch:
                root.dispatch("on_quad_touch")
            
            on_cursor_blink:
                root.dispatch("on_cursor_blink")
                
            on_cursor:
                root.dispatch("on_cursor")
                
            on_size:
                root.dispatch("on_size")
                
            on_handle_image_middle:
                root.dispatch("on_handle_image_middle")
                
            on_handle_image_left:
                root.dispatch("on_handle_image_left")
            
            on_handle_image_right:
                root.dispatch("on_handle_image_right")      
# kv_end
"""
)


class M_CardTextField(MDBoxLayout, ThemableBehavior):
    """
    This is a card text field that looks more like
    google website search textfield, you can use right_icon
    and left_icon with this widget and also add callback function to it

    read `Kivy TextInput doc` to understand more
    """

    elevation = NumericProperty(None, allownone=True)

    text_field_disabled = BooleanProperty(False)

    card_ripples = BooleanProperty(False)

    focus = BooleanProperty(False)

    input_type = StringProperty("text")

    icon_right_callback = ObjectProperty(lambda x: None)
    """[summary]
    simulates kivymd MDIconButton on_release method
    """

    hint_text_color = ColorProperty([0.5, 0.5, 0.5, 1.0])

    icon_left_disabled = BooleanProperty(False)

    icon_right_disabled = BooleanProperty(False)

    icon_left_callback = ObjectProperty(lambda x: None)
    """[summary]
    simulates kivymd MDIconButton on_release method
    """

    icon_right_color = ListProperty([0, 0, 0, 1])

    icon_left_color = ListProperty([0, 0, 0, 1])

    icon_left_font_size = NumericProperty(14)

    icon_right_font_size = NumericProperty(14)

    icon_right_font_name = StringProperty("")

    icon_left_font_name = StringProperty("")

    icon_right_background_color = ListProperty([0, 0, 0, 0])

    icon_left_background_color = ListProperty([0, 0, 0, 0])

    multiline = BooleanProperty(True)

    hint_text = StringProperty("")

    text = StringProperty("")

    radius = ListProperty([dp(10)])

    card_padding = NumericProperty(dp(10))

    card_spacing = NumericProperty(0)

    grow_card = BooleanProperty(True)

    background_disabled_normal = StringProperty("")

    text_field_background_normal = StringProperty("")

    text_field_background_active = StringProperty("")

    text_field_max_height = NumericProperty(dp(110))

    text_field_size_hint_y = NumericProperty(None, allownone=True)

    text_field_height = NumericProperty(None, allownone=True)

    cursor_color = ListProperty([1, 0, 0, 0.8])

    foreground_color = ListProperty([0, 0, 0, 0.8])

    disabled_foreground_color = ColorProperty([0, 0, 0, .5])

    input_filter = ObjectProperty(None, allownone=True)

    background_color = ColorProperty([1, 1, 1, 1])

    line_spacing = NumericProperty(0)

    allow_copy = BooleanProperty(True)

    replace_crlf = BooleanProperty(True)

    auto_indent = BooleanProperty(False)

    handle_image_middle = StringProperty(
        'atlas://data/images/defaulttheme/selector_middle')

    handle_image_left = StringProperty(
        'atlas://data/images/defaulttheme/selector_left')

    handle_image_right = StringProperty(
        'atlas://data/images/defaulttheme/selector_right')

    write_tab = BooleanProperty(True)

    base_direction = OptionProperty(None,
                                    options=['ltr', 'rtl',
                                             'weak_rtl', 'weak_ltr', None],
                                    allownone=True)

    font_family = StringProperty(None, allownone=True)

    font_context = StringProperty(None, allownone=True)

    font_size = NumericProperty('15sp')

    font_name = StringProperty(DEFAULT_FONT)

    selection_text = StringProperty(u'')

    readonly = BooleanProperty(False)

    text_validate_unfocus = BooleanProperty(True)

    password = BooleanProperty(False)

    password_mask = StringProperty('*')

    keyboard_suggestions = BooleanProperty(True)

    cursor_blink = BooleanProperty(True)

    cursor_width = NumericProperty('1sp')

    line_height = NumericProperty(1)

    tab_width = NumericProperty(4)

    text_field_padding = VariableListProperty([6, 6, 6, 6])

    halign = OptionProperty('auto', options=['left', 'center', 'right',
                                             'auto'])

    scroll_x = NumericProperty(0)

    scroll_y = NumericProperty(0)

    selection_color = ColorProperty([0.1843, 0.6549, 0.8313, .5])

    border = ListProperty([4, 4, 4, 4])

    use_bubble = BooleanProperty(not _is_desktop)

    use_handles = BooleanProperty(not _is_desktop)

    suggestion_text = StringProperty('')

    icon_left = StringProperty("")

    icon_right = StringProperty("")

    def __init__(self, **kwargs):
        self.icon_right_widget = MDIconButton(theme_text_color="Custom", text_color=[0, 0, 0, 1])
        self.icon_left_widget = MDIconButton(theme_text_color="Custom", text_color=[0, 0, 0, 1])
        super().__init__(**kwargs)
        self.register_event_type("on_text")
        self.register_event_type("on_triple_tap")
        self.register_event_type("on_double_tap")
        self.register_event_type("on_cursor_blink")
        self.register_event_type("on_cursor")
        self.register_event_type("on_size")
        self.register_event_type("on_handle_image_middle")
        self.register_event_type("on_handle_image_left")
        self.register_event_type("on_handle_image_right")
        self.register_event_type("on_text_validate")
        self.register_event_type("on_focus")
        self.register_event_type("on_quad_touch")
        self.register_event_type("on_release")
        if self.grow_card:
            self.multiline = True
        if self.icon_left:
            self.icon_left_widget = MDIconButton(
                icon=self.icon_left, on_release=self.icon_left_callback,
                md_bg_color=self.icon_left_background_color,
                theme_text_color="Custom", text_color=self.icon_left_color,
                font_name=self.icon_left_font_name, font_size=self.icon_left_font_size)
            self.add_widget(self.icon_left_widget, index=1)
            self.multiline = False

        if self.icon_right:
            self.icon_right_widget = MDIconButton(
                icon=self.icon_right, on_release=self.icon_right_callback,
                md_bg_color=self.icon_right_background_color,
                theme_text_color="Custom", text_color=self.icon_right_color,
                font_name=self.icon_right_font_name, font_size=self.icon_right_font_size)
            self.add_widget(self.icon_right_widget)
            # self.multiline = False

    def on_icon_left(self, instance, value):
        self.icon_left_widget.icon = value
        try:
            self.add_widget(self.icon_left_widget, index=1)
        except AttributeError:
            self.children.clear()
        self.multiline = False

    def on_icon_left_color(self, instance, value):
        self.icon_left_widget.text_color = value

    def on_icon_left_disabled(self, instance, value):
        self.icon_left_widget.disabled = value

    def on_icon_right_disabled(self, instance, value):
        self.icon_right_widget.disabled = value

    def on_icon_left_font_name(self, instance, value):
        self.icon_left_widget.font_name = value

    def on_icon_left_callback(self, instance, value):
        self.icon_left_widget.bind(on_release=value)

    def on_icon_left_font_size(self, instance, value):
        self.icon_widget.font_size = value

    def on_icon_left_background_color(self, instance, value):
        self.icon_widget.md_bg_color = value

    def on_icon_right(self, instance, value):
        self.icon_right_widget.icon = value
        try:
            self.add_widget(self.icon_right_widget)
        except AttributeError:
            self.children.clear()
        # self.multiline = False

    def on_icon_right_color(self, instance, value):
        self.icon_right_widget.text_color = value

    def on_icon_right_font_name(self, instance, value):
        self.icon_right_widget.font_name = value

    def on_icon_right_callback(self, instance, value):
        self.icon_right_widget.bind(on_release=value)

    def on_icon_right_font_size(self, instance, value):
        self.icon_right_widget.font_size = value

    def on_icon_right_background_color(self, instance, value):
        self.icon_right_widget.md_bg_color = value

    def on_text(self, *args):
        """[summary]
        simulates the on_text event in kivy default
        TextInput
        """

    def on_triple_tap(self):
        """[summary]
        simulates on_triple_tap event in kivy default
        TextInput
        """

    def on_double_tap(self):
        """[summary]
        simulates on_double_tap event in kivy default
        TextInput
        """

    def on_cursor_blink(self):
        """[summary]
        simulates on_cursor_blink event in kivy default
        TextInput
        """

    def on_cursor(self):
        """[summary]
        simulates on_cursor event in kivy default
        TextInput
        """

    def on_size(self, *args):
        """[summary]
        simulates on_size event in kivy default
        TextInput
        """

    def on_handle_image_middle(self):
        """[summary]
        simulates on_handle_image_middle event in kivy default
        TextInput
        """

    def on_handle_image_left(self):
        """[summary]
        simulates on_handle_image_left event in kivy default
        TextInput
        """

    def on_handle_image_right(self):
        """[summary]
        simulates on_handle_image_right event in kivy default
        TextInput
        """

    def on_text_validate(self):
        """[summary]
        simulates on_text_validate event in kivy default
        TextInput
        """

    def on_focus(self, *args):
        """[summary]
        simulates on_focus event in kivy default
        TextInput
        """

    def on_quad_touch(self):
        """[summary]
        simulates on_quad_touch event in kivy default
        TextInput
        """

    def on_release(self):
        """
        simulates MDCard on_release event
        """


if __name__ == "__main__":
    from kivymd.app import MDApp
    from kivy.uix.scrollview import ScrollView


    class Opera(MDApp):
        use_kivy_settings = False

        # kv_file = "main.kv"

        def build(self):
            root = MDBoxLayout(orientation='vertical', padding=dp(
                20), md_bg_color=[0, 0, 0, .15], spacing=dp(20))
            scroll = ScrollView()
            field = M_CardTextField(hint_text="text field with icon & can't grow", grow_card=False, multiline=False,
                                    md_bg_color=[1, 1, 1, 1], icon_right="magnify", icon_left="login",
                                    icon_left_callback=self.login, icon_right_callback=self.search
                                    )
            field2 = M_CardTextField(
                hint_text="text field with no icon & can grow", grow_card=True, elevation=0)

            field3 = M_CardTextField(hint_text="text field with right icon & can't grow", grow_card=False,
                                     icon_right="android",
                                     icon_right_color=[0, 1, 0, 1])
            field4 = M_CardTextField(hint_text="text field with left icon & can't grow", grow_card=False,
                                     icon_left="home",
                                     icon_left_color=[0, 0, 1, 1])
            root.add_widget(field)
            root.add_widget(field2)
            root.add_widget(field3)
            root.add_widget(field4)
            root.add_widget(scroll)
            return root

        def search(self, instance):
            print("searching", instance)

        def login(self, instance):
            print("login", instance)


    Opera().run()
