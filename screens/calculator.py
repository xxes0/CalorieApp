# screens/calculator.py
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast

import logic
from database import save_record

KV = """
<CalculatorScreen>:
    name: "calc"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Мой профиль"
            elevation: 0
            md_bg_color: 0.96, 0.97, 0.99, 1
            specific_text_color: 0.12, 0.16, 0.22, 1
            left_action_items: [["account-circle-outline", lambda x: None]]

        ScrollView:
            do_scroll_x: False
            bar_width: 0

            MDBoxLayout:
                orientation: "vertical"
                padding: "16dp"
                spacing: "14dp"
                size_hint_y: None
                height: self.minimum_height

                MDCard:
                    orientation: "vertical"
                    padding: "22dp"
                    spacing: "4dp"
                    size_hint_y: None
                    height: "160dp"
                    radius: [28, ]
                    elevation: 0
                    md_bg_color: 0.0, 0.58, 0.53, 1

                    MDLabel:
                        text: "🎯  ДНЕВНАЯ ЦЕЛЬ"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.75
                        font_style: "Overline"
                        bold: True
                        size_hint_y: None
                        height: self.texture_size[1]

                    Widget:
                        size_hint_y: None
                        height: "6dp"

                    MDLabel:
                        id: r_target
                        text: "—"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_style: "H1"
                        bold: True
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDLabel:
                        text: "ккал в сутки"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.75
                        font_style: "Body1"
                        size_hint_y: None
                        height: self.texture_size[1]

                MDCard:
                    orientation: "vertical"
                    padding: "20dp"
                    spacing: "12dp"
                    size_hint_y: None
                    height: self.minimum_height
                    radius: [28, ]
                    elevation: 0
                    md_bg_color: 1, 1, 1, 1

                    MDLabel:
                        text: "Баланс БЖУ"
                        font_style: "H6"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.16, 0.22, 1
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDGridLayout:
                        cols: 3
                        spacing: "8dp"
                        size_hint_y: None
                        height: "130dp"

                        MDCard:
                            orientation: "vertical"
                            padding: "8dp"
                            spacing: "4dp"
                            radius: [18, ]
                            elevation: 0
                            md_bg_color: 1.0, 0.93, 0.93, 1

                            MDIcon:
                                icon: "food-steak"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: 0.83, 0.18, 0.18, 1
                                font_size: "32sp"
                                size_hint_y: None
                                height: "36dp"

                            MDLabel:
                                id: r_p
                                text: "—"
                                halign: "center"
                                bold: True
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.83, 0.18, 0.18, 1
                                size_hint_y: None
                                height: self.texture_size[1]

                            MDLabel:
                                text: "Белки, г"
                                halign: "center"
                                theme_text_color: "Hint"
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]

                        MDCard:
                            orientation: "vertical"
                            padding: "8dp"
                            spacing: "4dp"
                            radius: [18, ]
                            elevation: 0
                            md_bg_color: 1.0, 0.96, 0.88, 1

                            MDIcon:
                                icon: "oil"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: 0.9, 0.55, 0.05, 1
                                font_size: "32sp"
                                size_hint_y: None
                                height: "36dp"

                            MDLabel:
                                id: r_f
                                text: "—"
                                halign: "center"
                                bold: True
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.9, 0.55, 0.05, 1
                                size_hint_y: None
                                height: self.texture_size[1]

                            MDLabel:
                                text: "Жиры, г"
                                halign: "center"
                                theme_text_color: "Hint"
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]

                        MDCard:
                            orientation: "vertical"
                            padding: "8dp"
                            spacing: "4dp"
                            radius: [18, ]
                            elevation: 0
                            md_bg_color: 0.9, 0.94, 1.0, 1

                            MDIcon:
                                icon: "bread-slice"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: 0.13, 0.42, 0.83, 1
                                font_size: "32sp"
                                size_hint_y: None
                                height: "36dp"

                            MDLabel:
                                id: r_c
                                text: "—"
                                halign: "center"
                                bold: True
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.13, 0.42, 0.83, 1
                                size_hint_y: None
                                height: self.texture_size[1]

                            MDLabel:
                                text: "Углев., г"
                                halign: "center"
                                theme_text_color: "Hint"
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]

                    MDBoxLayout:
                        size_hint_y: None
                        height: "24dp"
                        spacing: "8dp"

                        MDLabel:
                            id: r_bmr
                            text: "BMR: —"
                            theme_text_color: "Hint"
                            font_style: "Caption"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            id: r_tdee
                            text: "TDEE: —"
                            theme_text_color: "Hint"
                            font_style: "Caption"
                            halign: "right"
                            size_hint_y: None
                            height: self.texture_size[1]

                MDCard:
                    orientation: "vertical"
                    padding: "20dp"
                    spacing: "10dp"
                    size_hint_y: None
                    height: self.minimum_height
                    radius: [28, ]
                    elevation: 0
                    md_bg_color: 1, 1, 1, 1

                    MDLabel:
                        text: "Параметры"
                        font_style: "H6"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.16, 0.22, 1
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDTextField:
                        id: f_gender
                        hint_text: "Пол"
                        text: "Мужской"
                        readonly: True
                        mode: "rectangle"
                        icon_right: "gender-male-female"
                        on_focus: if self.focus: root.open_gender_menu()

                    MDTextField:
                        id: f_age
                        hint_text: "Возраст (лет)"
                        input_filter: "int"
                        mode: "rectangle"
                        icon_right: "calendar-account-outline"

                    MDTextField:
                        id: f_weight
                        hint_text: "Вес (кг)"
                        input_filter: "float"
                        mode: "rectangle"
                        icon_right: "scale-bathroom"

                    MDTextField:
                        id: f_height
                        hint_text: "Рост (см)"
                        input_filter: "float"
                        mode: "rectangle"
                        icon_right: "human-male-height-variant"

                    MDTextField:
                        id: f_activity
                        hint_text: "Активность"
                        text: "Средняя (3-5 тренировок в неделю)"
                        readonly: True
                        mode: "rectangle"
                        icon_right: "run-fast"
                        on_focus: if self.focus: root.open_activity_menu()

                    MDTextField:
                        id: f_goal
                        hint_text: "Цель"
                        text: "Поддержание веса"
                        readonly: True
                        mode: "rectangle"
                        icon_right: "target"
                        on_focus: if self.focus: root.open_goal_menu()

                MDFillRoundFlatIconButton:
                    text: "РАССЧИТАТЬ"
                    icon: "calculator-variant-outline"
                    pos_hint: {"center_x": .5}
                    md_bg_color: 0.0, 0.58, 0.53, 1
                    text_color: 1, 1, 1, 1
                    on_release: root.calculate()

                Widget:
                    size_hint_y: None
                    height: "16dp"
"""


class CalculatorScreen(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Builder.load_string(KV)

    def _build_menu(self, field_id, items, callback):
        field = self.ids[field_id]
        menu_items = [{
            "viewclass": "OneLineListItem",
            "text": t,
            "height": dp(56),
            "on_release": lambda x=t: callback(x),
        } for t in items]
        return MDDropdownMenu(caller=field, items=menu_items)

    def open_gender_menu(self):
        menu = self._build_menu(
            "f_gender", ["Мужской", "Женский"],
            lambda v: (setattr(self.ids.f_gender, "text", v),
                       setattr(self.ids.f_gender, "focus", False),
                       menu.dismiss()))
        menu.open()

    def open_activity_menu(self):
        menu = self._build_menu(
            "f_activity", list(logic.CalorieCalculator.ACTIVITY.keys()),
            lambda v: (setattr(self.ids.f_activity, "text", v),
                       setattr(self.ids.f_activity, "focus", False),
                       menu.dismiss()))
        menu.open()

    def open_goal_menu(self):
        menu = self._build_menu(
            "f_goal", list(logic.CalorieCalculator.GOALS.keys()),
            lambda v: (setattr(self.ids.f_goal, "text", v),
                       setattr(self.ids.f_goal, "focus", False),
                       menu.dismiss()))
        menu.open()

    def calculate(self):
        try:
            age, weight, height = logic.CalorieCalculator.validate(
                self.ids.f_age.text, self.ids.f_weight.text, self.ids.f_height.text)
        except ValueError as e:
            toast(str(e))
            return

        res = logic.CalorieCalculator.daily_norm(
            self.ids.f_gender.text, age, weight, height,
            self.ids.f_activity.text, self.ids.f_goal.text)

        self.ids.r_target.text = str(res["target"])
        self.ids.r_bmr.text = f"BMR: {res['bmr']} ккал"
        self.ids.r_tdee.text = f"TDEE: {res['tdee']} ккал"
        self.ids.r_p.text = f"{res['protein']}"
        self.ids.r_f.text = f"{res['fat']}"
        self.ids.r_c.text = f"{res['carbs']}"

        save_record(self.ids.f_gender.text, age, weight, height,
                    self.ids.f_activity.text, self.ids.f_goal.text, res["target"])
        toast("Сохранено в историю")

        try:
            from kivy.app import App
            App.get_running_app().refresh_history()
        except Exception:
            pass