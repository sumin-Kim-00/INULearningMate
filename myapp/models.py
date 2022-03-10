from operator import mod
from django.db import models

# Create your models here.
# To apply model change execute the following:
#   python manage.py makemigrations
#   python manage.py migrate

class App_Session(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    # session_data = models.TextField()
    # expire_date = models.DateTimeField()
    auto_login = models.BooleanField(default=False)

