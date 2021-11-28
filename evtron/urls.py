"""evtron URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

# from finance.views import finance_view

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('finance/', include('finance.urls')),
    # path('news/', include('news.urls')),
    path('', include('page.urls')),
    # path('product/', include('product.urls')),
    # path('project/', include('project.urls')),

    path('webmail/', RedirectView.as_view(url='https://www.pcjindustries.co.th:2096/')),
    path('whm/', RedirectView.as_view(url='https://www.pcjindustries.co.th:2087/')),

    # legacy path for this url 'index.php?tpid=0031&pgname=finance&count=1'
    # path('index.php/', finance_view, name='finance-view-2'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
