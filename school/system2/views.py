from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Lectures, classroom, Student, Announcement
from system1.models import User
from .forms import ClassroomForm, StudentForm, Score, Class_TeacherForm, StudentEditForm, AnnouncementForm
from django.db.models import Q, F, Avg, Sum
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    announcements = Announcement.objects.all()[:10]

    return render(request, 'sys1/home.html', {"announcements": announcements})


def announcement(request):
    form = AnnouncementForm(request.POST or None)
    if form.is_valid():
        acc = form.save(commit=False)
        acc.user = request.user
        acc.save()
        return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'sys1/announcement.html', context)


@login_required()
def lectureCreate(request):
    if request.method == 'POST':
        lec = request.POST.get("lecture")
        if lec != '' and lec is not None:
            newlec = Lectures(name=lec)
            newlec.save()

    context = {
        'Llists': Lectures.objects.all()
    }
    return render(request, 'sys1/lectureCreate.html', context)


@login_required()
def createClassRoom(request):
    context = {}
    form = ClassroomForm()
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            form = ClassroomForm()
    context = {
        'form': form,
        'classes': classroom.objects.all()
    }
    return render(request, 'sys1/createClassRoom.html', context)


@login_required()
def chooseClassroomRegister(request):
    context = {
        'classes': classroom.objects.all()
    }
    return render(request, 'sys1/chooseClassroomRegister.html', context)


@login_required()
def createStudent(request, id):
    class_ = classroom.objects.get(id=id)
    students = class_.student_set.all()
    lects = class_.lectures.all()
    lect = []
    if request.method == 'POST':
        print(request.POST.get("studentName") == '')
        stu = StudentForm(request.POST)
        if stu.is_valid():
            stu = stu.save(commit=False)
            stu.classRoom = class_
            stu.save()
            print(stu)
            for lectures in lects:
                lect.append(lectures)
            stu.lecture.add(*lect)
            # stu.lecture.save()
            for lec in lect:
                Score.objects.create(student=stu, lecture=lec)
        else:
            context = {
                'students': students,
                'form': stu
            }
            return render(request, 'sys1/createStudent.html', context)

    form = StudentForm()
    context = {
        'students': students,
        'form': form
    }

    return render(request, 'sys1/createStudent.html', context)


def studentList1(request):
    classes = classroom.objects.all().annotate(
        class_Avg=Avg('student__score__score'))
    context = {
        'classes': classes
    }
    return render(request, 'sys1/studentList1.html', context)


def studentsView(request, pk):
    clas = classroom.objects.get(id=pk)
    lectures = clas.lectures.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    print(q)
    # print("************************************")
    students = clas.student_set.filter(
        Q(name__icontains=q)
    ).annotate(avg=Avg('score__score'))
    context = {
        'students': students,
        'lectures': lectures
    }
    return render(request, 'sys1/studentsView.html', context)


def studentDetailAndEdit(request, pk):
    stu = Student.objects.get(id=pk)
    context = stu.score_set.all().aggregate(total=Avg('score'))
    context['student'] = stu
    form = StudentEditForm(request.POST or None, instance=stu)
    if form.is_valid():
        if request.user.admin:
            form.save()
        stu = Student.objects.get(id=pk)
        print("class room", stu.classRoom)
        if stu.lecture.all() != stu.classRoom.lectures.all():
            stu.lecture.clear()
            lectu = []
            for lect in stu.classRoom.lectures.all():
                lectu.append(lect)
            stu.lecture.add(*lectu)
            lectu = []
            for score in stu.score_set.all():
                lectu.append(score.lecture)
                if score.lecture not in stu.lecture.all():
                    score.delete()
                    lectu.pop()
            for lecture in stu.lecture.all():
                if lecture not in lectu:
                    Score.objects.create(student=stu, lecture=lecture)

    context['form'] = form

    return render(request, 'sys1/studentDetailAndEdit.html', context)


def chooseClassroomScoring(request):
    classes = classroom.objects.all().annotate(
        class_Avg=Avg('student__score__score'))
    user = request.user
    C_T = user.class_teacher_set.all().annotate(
        class_Avg=Avg('class_room__student__score__score'))
    for x in C_T:
        print(x.class_room)
    context = {
        'classes': classes,
        'C_T': C_T,
    }
    return render(request, 'sys1/chooseClassroomScoring.html', context)


@login_required()
def chooseLectureScoring(request, pk):
    clas = classroom.objects.get(id=pk)
    id = clas.id
    C_T = clas.class_teacher_set.filter(
        Q(Teacher=request.user) & Q(class_room=clas))
    lectures = clas.lectures.all()
    for x in C_T:
        print("----->", x.lecture.all())

    context = {
        'lectures': lectures,
        'id': id,
        'C_T': C_T,
    }
    return render(request, 'sys1/chooseLectureScoring.html', context)


def chooseStudentScoring(request, id, pk):
    clas = classroom.objects.get(id=pk)
    id = id
    students = clas.student_set.all()
    context = {
        'students': students,
        "id": id
    }
    # return render(request, 'chooseStudentScoring.html', {'message': 'hello wold'})
    return render(request, 'sys1/chooseStudentScoring.html', context)


def Scoring(request, id, pk, si):
    print(id, pk, si)
    score = Score.objects.get(Q(student__id=si) & Q(lecture__id=pk))
    q = request.GET.get('result') if request.GET.get(
        'result') != None else ''
    if score.score < 100 or '-' in q:
        if q != '':

            score.score = F('score') + int(q)
            score.save()
            score = Score.objects.get(Q(student__id=si) & Q(lecture__id=pk))

            return redirect('../../')

    context = {
        'score': score
    }
    print('------================------')
    return render(request, 'sys1/Scoring.html', context)


def assignment(request):
    form = Class_TeacherForm(request.POST or None)
    classes = classroom.objects.all()
    if form.is_valid():
        if request.user.admin:
            form.save()
        form = Class_TeacherForm()
    context = {
        'form': form,
        'classes': classes
    }
    return render(request, 'sys1/assignment.html', context)


def assignment_classchoice(request):
    classes = classroom.objects.all()
    context = {
        'classes': classes
    }
    return render(request, 'assignment_classchoice.html', context)


def assignment_detail(request, id):
    cls = classroom.objects.get(id=id)
    C_T = cls.class_teacher_set.all()
    context = {
        'C_T': C_T
    }
    return render(request, 'sys1/assignment_detail.html', context)
