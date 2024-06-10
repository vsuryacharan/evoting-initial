from django.contrib import admin
from django.urls import path,include
from .views import signup,my_view,login_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('signup',signup,name="signup"),
    path('logged_page',my_view,name="my_view"),
    path('',login_view,name="login_view"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)