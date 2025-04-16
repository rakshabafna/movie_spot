from django.db import models

from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    pass

class UserList(models.Model):
    user=models.ForeignKey(CustomUser, verbose_name="user", on_delete=models.CASCADE)
    name=models.CharField(max_length=250)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ListItem(models.Model):
    list=models.ForeignKey(UserList, verbose_name="user", on_delete=models.CASCADE)
    movie_name=models.CharField(max_length=250)
    movie_id=models.CharField(max_length=250)
    date_added=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Movie id:{self.movie_id} in {self.list}"


