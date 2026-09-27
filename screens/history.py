# screens/history.py
import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

from database import get_history, get_photo_history

# Глобальная ссылка на созданный экземпляр
_history_instance = None


def get_history_screen():
    return _history_instance


KV = """
<HistoryScreen>:
    name: "history"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "История"
            elevation: 0
            md_bg_color: 0.96, 0.97, 0.99, 1
            specific_text_color: 0.12, 0.16, 0.22, 1

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
                    padding: "20dp"
                    spacing: "8dp"
                    size_hint_y: None
                    height: self.minimum_height
                    radius: [28, ]
                    elevation: 0
                    md_bg_color: 1, 1, 1, 1

                    MDLabel:
                        text: "🔥  РАСЧЁТЫ НОРМЫ"
                        theme_text_color: "Hint"
                        font_style: "Overline"
                        bold: True
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDBoxLayout:
                        id: calc_list
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: "4dp"

                MDCard:
                    orientation: "vertical"
                    padding: "20dp"
                    spacing: "8dp"
                    size_hint_y: None
                    height: self.minimum_height
                    radius: [28, ]
                    elevation: 0
                    md_bg_color: 1, 1, 1, 1

                    MDLabel:
                        text: "🍽  РАСПОЗНАВАНИЯ"
                        theme_text_color: "Hint"
                        font_style: "Overline"
                        bold: True
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDBoxLayout:
                        id: photo_list
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: "4dp"

                Widget:
                    size_hint_y: None
                    height: "16dp"
"""


class HistoryScreen(MDScreen):
    def __init__(self, **kw):
        global _history_instance
        super().__init__(**kw)
        Builder.load_string(KV)
        _history_instance = self
        print("[history] HistoryScreen создан")

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        from kivymd.uix.list import (
            TwoLineAvatarIconListItem,
            ThreeLineAvatarIconListItem,
            IconLeftWidget,
            ImageLeftWidget,
            OneLineListItem,
        )

        print("[history] refresh() вызван")

        self.ids.calc_list.clear_widgets()
        self.ids.photo_list.clear_widgets()

        rows = get_history()
        print(f"[history] расчётов: {len(rows)}")
        if not rows:
            self.ids.calc_list.add_widget(
                OneLineListItem(text="Пока нет расчётов"))
        else:
            for row in rows:
                date, gender, age, weight, height, activity, goal, target = row
                item = TwoLineAvatarIconListItem(
                    text=f"{target} ккал / сутки",
                    secondary_text=f"{date}  •  {gender}, {age} лет, {weight} кг")
                item.add_widget(IconLeftWidget(
                    icon="fire",
                    theme_text_color="Custom",
                    text_color=(0.0, 0.58, 0.53, 1)))
                self.ids.calc_list.add_widget(item)

        rows = get_photo_history()
        print(f"[history] распознаваний: {len(rows)}")
        if not rows:
            self.ids.photo_list.add_widget(
                OneLineListItem(text="Пока нет распознаваний"))
        else:
            for row in rows:
                date, photo_path, rec, grams, total = row
                item = ThreeLineAvatarIconListItem(
                    text=f"{rec} — {total} ккал",
                    secondary_text=f"{grams} г",
                    tertiary_text=date)

                shown_image = False
                if photo_path and os.path.exists(photo_path):
                    try:
                        item.add_widget(ImageLeftWidget(source=photo_path))
                        shown_image = True
                    except Exception as exc:
                        print(f"[history] превью ошибка: {exc}")

                if not shown_image:
                    item.add_widget(IconLeftWidget(
                        icon="food",
                        theme_text_color="Custom",
                        text_color=(1.0, 0.76, 0.03, 1)))

                self.ids.photo_list.add_widget(item)