from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task,User

# Create your views here.


class TaskList(LoginRequiredMixin,ListView):
    model= Task
    template_name='home.html'
    context_object_name='tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        return context



class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    template_name='detail.html'
    context_object_name='task'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('home')
    template_name='create.html'

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('home')
    template_name='update.html'

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    success_url=reverse_lazy('home')
    context_object_name='task'
    template_name='delete.html'
    


def home(request):
    task=Task.objects.all()


    return render(request,'home.html',{'tasks' :task})

def Logout(request):

    logout(request)
    return redirect('/login')

def logon(request):

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        
        
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Please check Username and password")
            return redirect('login')

    else:
        return render(request,'login.html')

def register(request):

    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if(password1==password2):
            password=password2

            if(User.objects.filter(username=username).exists()):
                messages.info(request,"Username already exists")
                return redirect('register')
            elif(User.objects.filter(email=email).exists()):
                messages.info(request,"Email already exists")
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                user.save()
                return redirect('\login')
        else:
            messages.info(request,"Password Mismatch")
            return redirect('register')
        
    else:
        return render(request,'register.html')