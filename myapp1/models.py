from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Startup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    equity_offered = models.FloatField()
    valuation = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name


class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def _str_(self):
        return self.user.username


class Investment(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    equity_taken = models.FloatField()
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    invested_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.investor.user.username} invested in {self.startup.name}"



