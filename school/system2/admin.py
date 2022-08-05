from django.contrib import admin

# Register your models here.
from .models import *


# admin.site.register(User)
admin.site.register(classroom)
admin.site.register(Student)
admin.site.register(Lectures)
admin.site.register(Announcement)
# admin.site.register(Class_Teacher)
# admin.site.register(Score)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("student", 'score')
    ordering = ('student',)


@admin.register(Class_Teacher)
class Class_TeacherAdmin(admin.ModelAdmin):
    list_display = ('class_room', "Teacher")
    ordering = ('class_room',)
