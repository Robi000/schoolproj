from django import forms
from .models import *
from django.db.models import Q
from django.forms import ChoiceField, ModelChoiceField, ModelMultipleChoiceField, MultipleChoiceField, ValidationError
from system1.models import User


class ClassroomForm(forms.ModelForm):

    class Meta:
        model = classroom
        fields = ("grade", "section", "lectures")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lectures'].widget.attrs.update(
            {'class': "form-select my-3", "multiple": ""})
        self.fields['grade'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "grade"})
        self.fields['section'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "section"})

    def clean_section(self, *args, **kwargs):
        section = self.cleaned_data.get("section")
        grade = self.cleaned_data.get("grade")
        query_set = classroom.objects.filter(
            Q(grade=grade) &
            Q(section=section)
        )
        if query_set.__len__() != 0:
            raise ValidationError("you created same classroom !")
        return section.upper()


class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ('title', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "Title here"})
        self.fields['body'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "Body here"})


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'mother_full_name',
                  'Father_full_name', 'phone_no', 'Backup_phone_no', 'vaccinated']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': "form-control mb-2", "placeholder": "Name"})
        self.fields['mother_full_name'].widget.attrs.update(
            {'class': "form-control mb-2", "placeholder": "Mother name"})
        self.fields['Father_full_name'].widget.attrs.update(
            {'class': "form-control mb-2", "placeholder": "Father name"})
        self.fields['phone_no'].widget.attrs.update(
            {'class': "form-control mb-2", "placeholder": "09xxxxxxxx"})
        self.fields['Backup_phone_no'].widget.attrs.update(
            {'class': "form-control mb-2", "placeholder": "09xxxxxxxx"})
        self.fields['vaccinated'].widget.attrs.update(
            {'class': "form-check-input my-2"})


class StudentEditForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'mother_full_name', 'classRoom',
                  'Father_full_name', 'phone_no', 'Backup_phone_no', 'vaccinated']


class LecturesForm(forms.ModelForm):

    class Meta:
        model = Lectures
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "grade"})


class ScoreForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = '__all__'


class Class_TeacherForm(forms.ModelForm):
    Teacher = ModelChoiceField(queryset=User.objects.filter(admin=False))

    class Meta:
        model = Class_Teacher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lecture'].widget.attrs.update(
            {'class': "form-select my-3", "multiple": ""})
        self.fields['Teacher'].widget.attrs.update(
            {'class': "form-select my-3"})
        self.fields['class_room'].widget.attrs.update(
            {'class': "form-select my-3"})

    def clean(self):
        print(self.cleaned_data)
        a = self.cleaned_data.get("class_room")
        print(a)
        j = self.cleaned_data['lecture']
        q = Class_Teacher.objects.filter(
            Q(class_room=self.cleaned_data['class_room']) & Q(lecture__in=j))
        # print(q)

        if q.exists():
            qset = []
            setq = " existing teachers: "
            q = Class_Teacher.objects.filter(
                Q(class_room=self.cleaned_data['class_room']))
            for x in q:
                if x not in qset:
                    qset.append(x)
            self.add_error("lecture", setq)
            for x in qset:
                ad = ''
                for lec in x.lecture.all():
                    ad = ad + lec.name + ", "
                self.add_error(
                    "lecture", "- " + x.Teacher.first_name + " " + x.Teacher.last_name + ": " + ad)
            raise ValidationError("Check Teacher selection!")

        a = a.lectures.all()
        c = a
        a = set(a.values_list('id', flat=True))
        b = self.cleaned_data.get("lecture")
        b = set(b.values_list('id', flat=True))
        issub = b.issubset(a)
        print(issub)
        if not issub:
            b = ''
            for x in c:
                b += x.name + ', '
            self.add_error(
                'lecture', f"you selected wrong lectures for the class ({b})")
            raise ValidationError("Please fill the form correctly ")
        return self.cleaned_data
