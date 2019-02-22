from django.urls import path,include
from nutritionapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'nutritionapp'

urlpatterns = [
    path('strikers/',views.strikersview,name='strikersview'),
    path('processing/',views.processing,name='processing'),
    path('heat/',views.heatview,name='heatview'),
    path('hurricanes/',views.hurricanesview,name='hurricanesview'),
    path('renegades/',views.renegadesview,name='renegadesview'),
    path('stars/',views.starsview,name='starsview'),
    path('scorchers/',views.scorchersview,name='scorchersview'),
    path('thunders/',views.thundersview,name='thundersview'),
    path('sixers/',views.sixersview,name='sixersview'),
    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('profileedit/', views.profile_edit, name='profile_edit'),
    # path('addwater', views.addwater, name='addwater'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
