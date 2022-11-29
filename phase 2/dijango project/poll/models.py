from django.db import models

class Poll(models.Model):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def total(self):
        return (self.start_date, self.end_date)