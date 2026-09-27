# main.py
import os
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform

if platform == "android":
    from android.storage import app_storage_path
    DB_DIR = app_storage_path()
else:
    DB_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["CALORIE_DB_DIR"] = DB_DIR

from kivymd.app import MDApp

import database as db
from screens.calculator import CalculatorScreen
from screens.camera import CameraScreen
from screens.history import HistoryScreen, get_history_screen


KV = """
MDScreen:
    md_bg_color: 0.96, 0.97, 0.99, 1

    MDBottomNavigation:
        id: bottom_nav
        panel_color: 1, 1, 1, 1
        text_color_active: 0.0, 0.58, 0.53, 1
        text_color_normal: 0.55, 0.55, 0.60, 1

        MDBottomNavigationItem:
            name: "calc"
            text: "Калькулятор"
            icon: "calculator-variant-outline"
            CalculatorScreen:

        MDBottomNavigationItem:
            name: "camera"
            text: "Камера"
            icon: "camera-outline"
            CameraScreen:

        MDBottomNavigationItem:
            name: "history"
            text: "История"
            icon: "history"
            HistoryScreen:
"""


class CalorieApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        self.title = "Калькулятор калорий"

        Window.clearcolor = (0.96, 0.97, 0.99, 1)

        db.init_db()
        root = Builder.load_string(KV)

        # Экран истории создастся позже, поэтому обновляем с задержкой
        Clock.schedule_once(self._startup_refresh, 0.5)

        # Привязываем смену вкладок с задержкой
        Clock.schedule_once(self._bind_nav, 0.5)

        return root

    def _bind_nav(self, dt):
        try:
            nav = self.root.ids.bottom_nav
            nav.bind(current=self._on_tab_changed)
            print("[main] bind на bottom_nav выполнен")
        except Exception as exc:
            print(f"[main] bind error: {exc}")

    def _startup_refresh(self, dt):
        screen = get_history_screen()
        if screen:
            print("[main] стартовый refresh")
            try:
                screen.refresh()
            except Exception as exc:
                print(f"[main] стартовый refresh error: {exc}")
        else:
            print("[main] HistoryScreen ещё не создан")

    def _on_tab_changed(self, instance, value):
        print(f"[main] tab -> {value}")
        if value == "history":
            screen = get_history_screen()
            if screen:
                try:
                    screen.refresh()
                except Exception as exc:
                    print(f"[main] refresh error: {exc}")

    def refresh_history(self):
        screen = get_history_screen()
        if screen:
            try:
                screen.refresh()
            except Exception as exc:
                print(f"[main] refresh_history error: {exc}")


if __name__ == "__main__":
    CalorieApp().run()