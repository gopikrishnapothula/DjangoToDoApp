
from django.urls import path
from .views import TaskList,logon,register,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,Logout

urlpatterns = [
    
    path('',TaskList.as_view(),name="home"),
    path('task/<int:pk>',TaskDetail.as_view(),name="task"),
    path('create/',TaskCreate.as_view(),name="create"),
    path('update/<int:pk>',TaskUpdate.as_view(),name="update"),
    path('delete/<int:pk>',TaskDelete.as_view(),name="delete"),
    path('login/',logon,name="login"),
    path('logout/',Logout,name="logout"),
    path('register/',register,name="register"),
]