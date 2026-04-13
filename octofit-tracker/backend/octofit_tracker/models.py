from djongo import models

from bson import ObjectId

class Team(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False, db_column='_id')
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class User(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False, db_column='_id')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team_id = models.CharField(max_length=32)
    def __str__(self):
        return self.name

class Activity(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False, db_column='_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.user.name} - {self.activity}"

class Workout(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False, db_column='_id')
    name = models.CharField(max_length=100)
    suggested_for = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Leaderboard(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False, db_column='_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    points = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.user.name} - {self.points} pts"
