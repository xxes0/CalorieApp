# calculator.py
# Модуль расчёта суточной нормы калорий.
# Используется формула Миффлина — Сан Жеора (2005), признанная ВОЗ.


class CalorieCalculator:
    """Класс для расчёта базового метаболизма и суточной нормы калорий."""

    # Коэффициенты физической активности
    ACTIVITY = {
        "Минимальная (сидячий образ жизни)": 1.2,
        "Низкая (1–2 тренировки в неделю)": 1.375,
        "Средняя (3–5 тренировок в неделю)": 1.55,
        "Высокая (6–7 тренировок в неделю)": 1.725,
        "Очень высокая (спортсмены, физ. работа)": 1.9,
    }

    # Цели
    GOALS = {
        "Похудение (-20%)": 0.8,
        "Поддержание веса": 1.0,
        "Набор массы (+15%)": 1.15,
    }

    @staticmethod
    def validate(age, weight, height):
        """Проверка корректности введённых данных."""
        try:
            age = int(age)
            weight = float(weight)
            height = float(height)
        except (ValueError, TypeError):
            raise ValueError("Все поля должны содержать числа.")

        if not (10 <= age <= 120):
            raise ValueError("Возраст должен быть от 10 до 120 лет.")
        if not (25 <= weight <= 300):
            raise ValueError("Вес должен быть от 25 до 300 кг.")
        if not (100 <= height <= 250):
            raise ValueError("Рост должен быть от 100 до 250 см.")
        return age, weight, height

    @classmethod
    def bmr(cls, gender, age, weight, height):
        """Базовый метаболизм (BMR) по формуле Миффлина — Сан Жеора."""
        if gender == "Мужской":
            return 10 * weight + 6.25 * height - 5 * age + 5
        return 10 * weight + 6.25 * height - 5 * age - 161

    @classmethod
    def daily_norm(cls, gender, age, weight, height, activity_key, goal_key):
        """Полный расчёт: BMR → TDEE → норма под цель."""
        base = cls.bmr(gender, age, weight, height)
        tdee = base * cls.ACTIVITY[activity_key]
        norm = tdee * cls.GOALS[goal_key]
        return {
            "bmr": round(base),
            "tdee": round(tdee),
            "target": round(norm),
            "protein": round(norm * 0.30 / 4),   # 30% белков, 4 ккал/г
            "fat": round(norm * 0.30 / 9),       # 30% жиров, 9 ккал/г
            "carbs": round(norm * 0.40 / 4),     # 40% углеводов, 4 ккал/г
        }