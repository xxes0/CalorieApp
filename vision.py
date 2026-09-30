# vision.py
# Офлайн-распознавание еды. Поддерживает все форматы изображений, которые умеет PIL.

import json
import os
from kivy.utils import platform
from PIL import Image

try:
    import numpy as np
except ImportError:
    np = None

try:
    from ai_edge_litert.interpreter import Interpreter
except ImportError:
    try:
        from tflite_runtime.interpreter import Interpreter
    except ImportError:
        try:
            from tensorflow.lite.python.interpreter import Interpreter
        except ImportError:
            Interpreter = None

# Регистрируем поддержку HEIC/HEIF (фото iPhone), если установлен pillow-heif
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

# Регистрируем поддержку AVIF, если установлен pillow-avif
try:
    import pillow_avif  # noqa
except ImportError:
    pass


def _assets_dir():
    if platform == "android":
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), "assets")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


MODEL_PATH = os.path.join(_assets_dir(), "food_model.tflite")
LABELS_PATH = os.path.join(_assets_dir(), "labels_ru.json")


class VisionError(Exception):
    pass


_interpreter = None
_labels = None
_input_is_uint8 = False
_input_size = (224, 224)


def _load():
    global _interpreter, _labels, _input_is_uint8, _input_size
    if _interpreter is not None:
        return

    if np is None:
        raise VisionError("Не установлен numpy. Выполните: pip install numpy")
    if Interpreter is None:
        raise VisionError(
            "Не установлен TFLite. Выполните: pip install ai-edge-litert")
    if not os.path.exists(MODEL_PATH):
        raise VisionError("Модель food_model.tflite не найдена в папке assets/.")
    if not os.path.exists(LABELS_PATH):
        raise VisionError("Файл labels_ru.json не найден в папке assets/.")

    _interpreter = Interpreter(model_path=MODEL_PATH)
    _interpreter.allocate_tensors()

    inp = _interpreter.get_input_details()[0]
    _input_is_uint8 = (inp["dtype"] == np.uint8)
    h, w = inp["shape"][1], inp["shape"][2]
    _input_size = (w, h)

    with open(LABELS_PATH, encoding="utf-8") as f:
        _labels = json.load(f)


def open_image_any(path: str) -> Image.Image:
    """
    Открывает изображение любого формата и возвращает PIL-объект в RGB.
    Бросает VisionError с понятным сообщением, если формат не поддержан.
    """
    if not os.path.exists(path):
        raise VisionError("Файл не найден.")

    try:
        img = Image.open(path)
    except Exception:
        ext = os.path.splitext(path)[1].lower()
        raise VisionError(
            f"Не удалось открыть файл формата {ext}. "
            "Попробуйте сохранить изображение как JPG или PNG."
        )

    # Некоторые форматы (GIF, TIFF) могут быть многокадровыми — берём первый кадр
    try:
        img.seek(0)
    except (AttributeError, EOFError):
        pass

    if img.mode != "RGB":
        img = img.convert("RGB")

    return img


def recognize_food(image_path: str) -> str:
    # На Android распознавание не поддерживается без TFLite
    if platform == "android":
        raise VisionError(
            "Распознавание по фото доступно только в Windows-версии.\n"
            "На Android TFLite требует отдельной сборки."
        )

    _load()
    img = open_image_any(image_path)
    img = img.resize(_input_size)

    if _input_is_uint8:
        data = np.asarray(img, dtype=np.uint8)
        data = np.expand_dims(data, axis=0)
    else:
        data = np.asarray(img, dtype=np.float32) / 255.0
        data = np.expand_dims(data, axis=0)

    inp = _interpreter.get_input_details()
    out = _interpreter.get_output_details()

    _interpreter.set_tensor(inp[0]["index"], data)
    _interpreter.invoke()
    output = _interpreter.get_tensor(out[0]["index"])[0]

    idx = int(np.argmax(output))
    keys = list(_labels.keys())
    if idx >= len(keys):
        raise VisionError(
            f"Индекс {idx} вне списка меток ({len(keys)}). "
            "Модель и labels_ru.json не совпадают."
        )
    return _labels[keys[idx]]
