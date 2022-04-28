from typing import Sequence, Union


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training(object):
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.speed = self.get_distance() / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action,
                 duration,
                 weight
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        coeff_calorie_3: int = 60
        spent_calories = ((coeff_calorie_1 * self.get_mean_speed()
                          - coeff_calorie_2)
                          * self.weight / self.M_IN_KM
                          * self.duration * coeff_calorie_3)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action,
                 duration,
                 weight,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        coeff_walking_1: float = 0.035
        coeff_walking_2: float = 0.029
        coeff_walking_3: int = 60
        spent_calories = ((coeff_walking_1
                          * self.weight + (self.get_mean_speed()**2
                           // self.height) * coeff_walking_2 * self.weight)
                          * self.duration * coeff_walking_3)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool,
                 count_pool
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_spent_calories(self) -> float:
        coeff_swim_calorie_1: float = 1.1
        coeff_swim_calorie_2: int = 2
        spent_calories = ((self.get_mean_speed() + coeff_swim_calorie_1)
                          * coeff_swim_calorie_2 * self.weight)
        return spent_calories

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed


def read_package(workout_type: str,
                 data: Sequence[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_codes: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_codes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(info.get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
