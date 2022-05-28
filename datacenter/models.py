import datetime

from django.db import models
from django.utils.timezone import make_aware


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def get_duration(self):
        if self.leaved_at is None:
            return make_aware(datetime.datetime.now()) - self.entered_at
        else:
            return self.leaved_at - self.entered_at

    def format_duration(self):
        format_duration = ':'.join(str(self.get_duration()).split(':')[:2])
        return format_duration

    def is_visit_long(self, minutes=60):
        duration = self.get_duration()
        duration_in_minutes = duration.total_seconds() // 60
        return True if duration_in_minutes >= minutes else False

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
