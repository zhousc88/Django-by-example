from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from braces.views import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.

class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_invalid(self, form):
        result = super(StudentRegistrationView, self).form_valid(form)
        data = form.cleaned_data
        user =authenticate(username=data['username'],password=data['password'])
        login(self.request,user)
        return result

class StudentEnrollCourseView(LoginRequiredMixin,FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView,self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',args=[self.course.id])

class StudentCourseListView(LoginRequiredMixin,ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(student__in=[self.request.user])

class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs= super(StudentCourseDetailView,self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self,**kwargs):
        context = super(StudentCourseDetailView,self).get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] =  course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all()
        return context