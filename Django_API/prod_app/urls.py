from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.protected_route),
    path('login/', views.login_view),
    path('carecloud/', views.carecloud),
    path('mis/', views.mis),
    path('fox/', views.fox),
    path('globalportal/', views.globalportal),
    path('direct/', views.director),
]
