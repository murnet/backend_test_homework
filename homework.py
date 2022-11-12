class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {round(self.duration, 3):.3f} ч.; "
            f"Дистанция: {round(self.distance, 3):.3f} км; "
            f"Ср. скорость: {round(self.speed, 3):.3f} км/ч; "
            f"Потрачено ккал: {round(self.calories, 3):.3f}."
        )
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result = self.action * self.LEN_STEP / self.M_IN_KM
        return result

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result = self.get_distance() / self.duration
        return result

    def get_spent_calories(self) -> float:  # расчет в дочерних классах
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return info


class Running(Training):
    """Тренировка: бег."""

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        coeff_calorie_1: float = 18,
        coeff_calorie_2: float = 20,
    ) -> None:
        super().__init__(action, duration, weight)
        self.coeff_calorie_1 = coeff_calorie_1
        self.coeff_calorie_2 = coeff_calorie_2

    def get_spent_calories(self) -> float:
        mean_speed = super().get_mean_speed()
        duration = self.duration * 60

        result = (
            (self.coeff_calorie_1 * mean_speed - self.coeff_calorie_2)
            * self.weight
            / self.M_IN_KM
            * duration
        )
        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
        coeff_calorie_1: float = 0.035,
        coeff_calorie_2: float = 0.029,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.coeff_calorie_1 = coeff_calorie_1
        self.coeff_calorie_2 = coeff_calorie_2

    def get_spent_calories(self) -> float:
        mean_speed = super().get_mean_speed()
        duration = self.duration * 60

        result = (
            self.coeff_calorie_1 * self.weight
            + (mean_speed**2 // self.height)
            * self.coeff_calorie_2
            * self.weight
        ) * duration
        return result


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
        coeff_calorie_1: float = 1.1,
        coeff_calorie_2: float = 2,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.coeff_calorie_1 = coeff_calorie_1
        self.coeff_calorie_2 = coeff_calorie_2

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result = self.action * self.LEN_STEP / self.M_IN_KM
        return result

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return result

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()

        result = (
            (mean_speed + self.coeff_calorie_1)
            * self.coeff_calorie_2
            * self.weight
        )
        return result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_mapper = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    try:
        return class_mapper[workout_type](*data)
    except KeyError:
        print(
            f"Данного кода тренировки ('{workout_type}') - не существует, "
            "выберите один из слудующих - 'SWM', 'RUN', 'WLK'"
        )


def main(training: Training) -> None:
    """Главная функция."""
    try:
        info = training.show_training_info()
        print(info.get_message())
    except AttributeError:
        pass


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
        ("ADFA", [1500, 22, 43, 23]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
