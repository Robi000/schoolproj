from django.urls import path

from . import views


urlpatterns = [
    path("announcement/", views.announcement, name='announcement'),
    path("assignment/", views.assignment, name='assignment'),
    path("assignment/class_choice/",
         views.assignment_classchoice, name='assignmentClsCho'),
    path("assignment/class_choice/<int:id>/",
         views.assignment_detail, name='assignmentDetail'),
    path("lectureCreate/", views.lectureCreate, name='lectureCreate'),
    path("createClassRoom/", views.createClassRoom, name='createClassRoom'),
    path("chooseClassroomRegister/",
         views.chooseClassroomRegister, name='chooseClassroomRegister'),
    path("<int:id>/createStudent/", views.createStudent, name='createStudent'),

    path("classrooms/", views.studentList1, name='classrooms'),
    path("classrooms/<int:pk>/studentsView/",
         views.studentsView, name='studentsView'),
    path("", views.home, name='home'),
    path("<int:pk>/studentDetailAndEdit/",
         views.studentDetailAndEdit, name='studentDetailAndEdit'),
    path("score/", views.chooseClassroomScoring, name="chooseClassroomScoring"),
    path("score/<int:pk>/lecture/", views.chooseLectureScoring,  # pk = class id
         name="chooseLectureScoring"),
    path("score/<int:pk>/lecture/<int:id>/student/", views.chooseStudentScoring,  # pk = class id
         name="chooseStudentScoring"),
    path("score/<int:id>/lecture/<int:pk>/student/<int:si>/Scoring/", views.Scoring,  # id - class pk lecture si student id
         name="Scoring"),
    #     path("score/<int:id>/lecture/<int:pk>/student/Scoring/", views.Scoring,  # id - lectuer pk for studet
    #          name="Scoring"),
]
