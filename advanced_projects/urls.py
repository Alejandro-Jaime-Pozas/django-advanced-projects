"""
URL configuration for advanced_projects project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')), # this ensures blog website starts at https://localhost:8000/ vs some other endpoint
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # THIS IS USED IF APP IS BEING DEPLOYED W/STATIC AND MEDIA FILES THROUGH DJANGO, NOT NEEDED FOR SERVER SIDE IF FILES SCPECIFIED IN SERVER CONFIG; media root is where the servable files live, media url is where those files will be accessed by user through browser; for the static files, it's a separate setting and folder to adhere to security practices