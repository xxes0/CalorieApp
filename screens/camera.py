# screens/camera.py
import os
import tempfile
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast

import vision
import foods_data
from database import save_photo_record

IMAGE_EXTENSIONS = [
    "*.jpg", "*.jpeg", "*.jpe", "*.jfif",
    "*.png", "*.gif", "*.bmp", "*.webp",
    "*.tif", "*.tiff", "*.ico",
    "*.ppm", "*.pgm", "*.pbm", "*.pnm",
    "*.heic", "*.heif", "*.avif",
]

TK_FILETYPES = [
    ("Все изображения", " ".join(IMAGE_EXTENSIONS)),
    ("JPEG", "*.jpg *.jpeg *.jpe *.jfif"),
    ("PNG", "*.png"),
    ("WebP", "*.webp"),
    ("HEIC / HEIF", "*.heic *.heif"),
    ("Все файлы", "*.*"),
]

KV = """
<CameraScreen>:
    name: "camera"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Анализ блюда"
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

                # ==== ПРЕВЬЮ ====
                MDCard:
                    size_hint_y: None
                    height: "280dp"
                    radius: [28, ]
                    elevation: 0
                    md_bg_color: 1, 1, 1, 1

                    Image:
                        id: preview
                        source: ""
                        fit_mode: "contain"

                # ==== КНОПКИ ====
                MDBoxLayout:
                    size_hint_y: None
                    height: "48dp"
                    spacing: "10dp"

                    MDFillRoundFlatIconButton:
                        text: "КАМЕРА"
                        icon: "camera"
                        size_hint_x: .5
                        md_bg_color: 0.0, 0.58, 0.53, 1
                        text_color: 1, 1, 1, 1
                        on_release: root.take_shot()

                    MDFillRoundFlatIconButton:
                        text: "ГАЛЕРЕЯ"
                        icon: "image-multiple-outline"
                        size_hint_x: .5
                        md_bg_color: 1.0, 0.76, 0.03, 1
                        text_color: 0.15, 0.15, 0.15, 1
                        on_release: root.pick_from_gallery()

                # ==== РЕЗУЛЬТАТ ====
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
                        text: "🍽  РАСПОЗНАНО"
                        theme_text_color: "Hint"
                        font_style: "Overline"
                        bold: True
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDLabel:
                        id: r_recognized
                        text: "Наведи камеру на блюдо"
                        halign: "center"
                        font_style: "H5"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.0, 0.58, 0.53, 1
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDLabel:
                        id: r_kcal100
                        text: "Калорийность появится здесь"
                        halign: "center"
                        theme_text_color: "Hint"
                        font_style: "Body2"
                        size_hint_y: None
                        height: self.texture_size[1]

                    Widget:
                        size_hint_y: None
                        height: "8dp"

                    MDSeparator:
                        height: "1dp"

                    Widget:
                        size_hint_y: None
                        height: "8dp"

                    MDLabel:
                        text: "Порция"
                        theme_text_color: "Hint"
                        font_style: "Caption"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDSlider:
                        id: grams
                        min: 10
                        max: 800
                        value: 200
                        color: 0.0, 0.58, 0.53, 1
                        on_value: root.on_grams(self.value)

                    MDLabel:
                        id: r_grams
                        text: "200 г"
                        halign: "center"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]

                    Widget:
                        size_hint_y: None
                        height: "6dp"

                    MDLabel:
                        id: r_total
                        text: "—"
                        halign: "center"
                        font_style: "H1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.0, 0.58, 0.53, 1
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDLabel:
                        text: "ккал в выбранной порции"
                        halign: "center"
                        theme_text_color: "Hint"
                        font_style: "Caption"
                        size_hint_y: None
                        height: self.texture_size[1]

                    Widget:
                        size_hint_y: None
                        height: "8dp"

                    MDFillRoundFlatIconButton:
                        text: "СОХРАНИТЬ"
                        icon: "content-save-outline"
                        pos_hint: {"center_x": .5}
                        md_bg_color: 0.0, 0.58, 0.53, 1
                        text_color: 1, 1, 1, 1
                        on_release: root.save_result()

                Widget:
                    size_hint_y: None
                    height: "16dp"
"""


class CameraScreen(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Builder.load_string(KV)
        self._photo_path = None
        self._recognized = None
        self._kcal100 = None

    def take_shot(self):
        if platform != "android":
            self.pick_from_gallery()
            return

        # Разрешения
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE])

        try:
            from jnius import autoclass, cast
            from android import activity

            Intent = autoclass('android.content.Intent')
            MediaStore = autoclass('android.provider.MediaStore')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            current_activity = PythonActivity.mActivity
            current_activity.startActivityForResult(intent, 1001)

            # Слушаем результат
            def on_activity_result(request_code, result_code, data):
                if request_code != 1001:
                    return
                try:
                    if data is None:
                        toast("Снимок отменён")
                        return
                    extras = data.getExtras()
                    bitmap = extras.get("data")
                    if bitmap is None:
                        toast("Не удалось получить снимок")
                        return

                    # Сохраняем bitmap в файл
                    import tempfile
                    from jnius import cast
                    FileOutputStream = autoclass('java.io.FileOutputStream')
                    Bitmap = autoclass('android.graphics.Bitmap')
                    CompressFormat = autoclass('android.graphics.Bitmap$CompressFormat')

                    path = os.path.join(tempfile.gettempdir(), "food_shot.jpg")
                    stream = FileOutputStream(path)
                    bitmap.compress(CompressFormat.JPEG, 85, stream)
                    stream.flush()
                    stream.close()

                    Clock.schedule_once(lambda dt: self._process(path))
                except Exception as exc:
                    msg = str(exc)
                    Clock.schedule_once(lambda dt: toast(f"Ошибка: {msg}"))

            activity.bind(on_activity_result=on_activity_result)

        except Exception as exc:
            toast(f"Камера недоступна: {exc}")
        else:
            self.pick_from_gallery()

    def _on_shot(self, path):
        if not path:
            toast("Снимок не сделан")
            return
        Clock.schedule_once(lambda dt: self._process(path))

    def pick_from_gallery(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE,
                                 Permission.READ_MEDIA_IMAGES])
            try:
                from plyer import filechooser
                filechooser.open_file(
                    filters=IMAGE_EXTENSIONS,
                    multiple=False,
                    on_selection=self._on_file_selected)
            except Exception as exc:
                toast(f"Галерея недоступна: {exc}")
        else:
            import threading
            threading.Thread(target=self._pick_windows, daemon=True).start()

    def _on_file_selected(self, selection):
        if not selection:
            return
        path = selection[0] if isinstance(selection, (list, tuple)) else selection
        Clock.schedule_once(lambda dt: self._process(path))

    def _pick_windows(self):
        try:
            from tkinter import Tk, filedialog
            root = Tk()
            root.withdraw()
            path = filedialog.askopenfilename(
                title="Выберите изображение",
                filetypes=TK_FILETYPES)
            root.destroy()
            if path:
                Clock.schedule_once(lambda dt: self._process(path))
        except Exception as exc:
            msg = str(exc)
            Clock.schedule_once(lambda dt: toast(f"Ошибка: {msg}"))

    def _process(self, path):
        # Показываем картинку в любом случае
        self._photo_path = path
        self.ids.preview.source = path
        self.ids.preview.reload()

        # Пытаемся распознать — если не получится, покажем ошибку
        toast("Распознаём…")
        Clock.schedule_once(lambda dt: self._recognize(path), 0.1)

    def _recognize(self, path):
        try:
            name = vision.recognize_food(path)
        except vision.VisionError as exc:
            toast(str(exc))
            return
        except Exception as exc:
            toast(f"Ошибка: {exc}")
            return

        matched, kcal100 = foods_data.find_kcal(name)
        self._recognized = name
        self._kcal100 = kcal100

        self.ids.r_recognized.text = name
        if kcal100:
            self.ids.r_kcal100.text = f"≈ {kcal100} ккал на 100 г"
            self._recalc()
        else:
            self.ids.r_kcal100.text = "Нет в справочнике калорийности"
            self.ids.r_total.text = "—"

    def on_grams(self, value):
        self.ids.r_grams.text = f"{int(value)} г"
        self._recalc()

    def _recalc(self):
        if not self._kcal100:
            return
        grams = self.ids.grams.value
        self.ids.r_total.text = f"{round(self._kcal100 * grams / 100)}"

    def save_result(self):
        if not self._recognized or not self._kcal100:
            toast("Сначала распознайте фото")
            return
        grams = int(self.ids.grams.value)
        total = round(self._kcal100 * grams / 100)
        save_photo_record(self._photo_path, self._recognized,
                          self._recognized, grams, total)
        toast(f"Сохранено: {total} ккал")

        # Обновить экран истории сразу
        try:
            from kivy.app import App
            App.get_running_app().refresh_history()
        except Exception:
            pass
