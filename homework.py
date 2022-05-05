from dataclasses import dataclass
from typing import Sequence, Type
import typing


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return ("Тип тренировки: {}; "
                "Длительность: {:.3f} ч.; "
                "Дистанция: {:.3f} км; "
                "Ср. скорость: {:.3f} км/ч; "
                "Потрачено ккал: {:.3f}.".format(
                    self.training_type, self.duration, self.distance,
                    self.speed, self.calories)
                )


class Training(object):
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: float = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUN_CAL_МULT: float = 18
    RUN_CAL_INCR: float = 20

    def get_spent_calories(self) -> float:
        return (
            (
                self.RUN_CAL_МULT * self.get_mean_speed() - self.RUN_CAL_INCR
            )
            * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_CAL_WGTH_MULT: float = 0.035
    WALK_CAL_SPEED_MULT: float = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        return (
            (
                self.WALK_CAL_WGTH_MULT * self.weight
                + (
                    self.get_mean_speed()**2 // self.height
                  )
                * self.WALK_CAL_SPEED_MULT * self.weight
            )
            * self.duration * self.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_CAL_INCR: float = 1.1
    SWIM_CAL_MULT: float = 2

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
        return ((self.get_mean_speed() + self.SWIM_CAL_INCR)
                * self.SWIM_CAL_MULT * self.weight)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str,
                 data: Sequence[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_codes: typing.Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_codes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
