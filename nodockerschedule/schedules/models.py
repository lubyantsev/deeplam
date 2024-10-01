from django.db import models


class Schedule(models.Model):
    objects = None
    name = models.CharField(max_length=100)  # Имя участника
    time = models.DateTimeField()  # Время
    location = models.CharField(max_length=100)  # Место
    password = models.CharField(max_length=100, blank=True)  # Пароль для доступа к расписанию
    is_booked = models.BooleanField(default=False)  # Статус бронирования

    def __str__(self):
        return f'{self.name} - {self.time} - {self.location}'


class Event(models.Model):
    objects = None
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    time = models.DateTimeField()
    place = models.CharField(max_length=100)
    participant_name = models.CharField(max_length=100, blank=True, null=True)

    def is_free(self):
        return self.participant_name is None
