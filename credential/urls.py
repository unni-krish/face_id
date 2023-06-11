from . import views
from django.urls import path
app_name='face'

urlpatterns = [

    path('signup/',views.signup,name='signup'),
    path('',views.login,name='login'),
    path('face_id/',views.face_id,name='face_id'),
    path('logout/',views.logout,name='logout')
]