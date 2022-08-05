from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.


class Class_Teacher(models.Model):
    class_room = models.ForeignKey(
        "system2.classroom",  on_delete=models.CASCADE)
    Teacher = models.ForeignKey("system1.User", on_delete=models.CASCADE)
    lecture = models.ManyToManyField(
        "system2.Lectures", related_name="room_lecture")


class classroom(models.Model):
    grade = models.IntegerField()
    section = models.CharField(max_length=2)
    lectures = models.ManyToManyField(
        "system2.Lectures", related_name="lectures")

    class Meta:
        ordering = ["grade", "section"]

    def __str__(self):
        return str(self.grade) + self.section


class Student(models.Model):
    phone_regx = RegexValidator(
        regex=r'^\+?0?\d{10,13}$', message='Phone number must be in correct form +2519xxxxxxxx')
    name = models.CharField(max_length=50, blank=False, null=False)
    lecture = models.ManyToManyField(
        "system2.Lectures", related_name='lecture')
    classRoom = models.ForeignKey(
        "system2.classroom",  on_delete=models.CASCADE, null=True)
    mother_full_name = models.CharField(max_length=50, blank=False, null=True)
    Father_full_name = models.CharField(max_length=50, blank=False, null=True)
    phone_no = models.CharField(
        validators=[phone_regx], max_length=50, null=True)
    Backup_phone_no = models.CharField(
        validators=[phone_regx], max_length=50, null=True)
    vaccinated = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Lectures(models.Model):
    name = models.CharField(max_length=50)
    # score = models.IntegerField(null=True, blank=False)

    def __str__(self) -> str:
        return self.name


class Score (models.Model):
    student = models.ForeignKey(
        "system2.Student", on_delete=models.CASCADE)
    score = models.IntegerField(null=True, default=0)
    lecture = models.ForeignKey("system2.Lectures", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student.id) + " )  " + self.student.name


class Announcement(models.Model):
    user = models.ForeignKey("system1.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title
