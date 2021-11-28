from django.shortcuts import render
# from news.views import news_list
# from project.views import project_list
from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.templatetags.static import static
from django.template.defaultfilters import truncatechars

import os
import datetime

# Create your views here.
def page_home(request):
    # news_queryset = news_list(request, 2)
    # project_queryset = project_list(request, 6)
    # AGE = datetime.datetime.now().year-1998

    # LANG = get_language()
    # path = os.path.join(settings.STATICFILES_DIRS[0], 'images', 'carousel', LANG)
    # carousel_images = os.listdir(path)
    # for i, img in enumerate(carousel_images):
    #     carousel_images[i] = 'images/carousel/'+ LANG + '/' + img

    # return render(request, 'page/page_home.html' , {
    #     'news_queryset': news_queryset,
    #     'project_queryset': project_queryset,
    #     'carousel_images': carousel_images,
    #     'AGE': AGE,
    #     'meta_title': _('pcj-industries-long'),
    #     'meta_desc': _('meta-desc-home'),
    #     'meta_kw': _('meta-kw-home'),
    #     'meta_img': request.build_absolute_uri(static('images/pcj-logo-og.jpg')),
    #     'meta_robots': 'index, follow',
    # })
    return render(request, 'page/page_home.html' , {
    })

def page_about(request):
    path = os.path.join(settings.STATICFILES_DIRS[0], 'images', 'factory')
    factory_images = sorted(os.listdir(path))
    for i, img in enumerate(factory_images):
        factory_images[i] = 'images/factory/' + img

    return render(request, 'page/page_about.html' , {
        'factory_images': factory_images,
        'meta_title': _('about').capitalize(),
        'meta_desc': truncatechars(_('about-us-content-1'), 200),
        'meta_kw': _('meta-kw-home'),
        'meta_img': request.build_absolute_uri(static('images/factory/006.jpg')),
        'meta_robots': 'index, nofollow',
    })

def page_contact(request):
    return render(request, 'page/page_contact.html', {
        'meta_title': _('contact').capitalize(),
        'meta_desc': _('pcj-industries-full')+" "+ \
                     _('pcj-office-road')+" "+ \
                     _('pcj-office-area')+" "+ \
                     _('pcj-office-province'),
        'meta_kw': _('meta-kw-home'),
        'meta_img': request.build_absolute_uri(static('images/pcj-logo-og.jpg')),
        'meta_robots': 'index, nofollow',
    })

def page_career(request):
    return render(request, 'page/page_career.html', {
        'meta_title': _('career').capitalize(),
        'meta_desc': truncatechars(_('career-content-1')+" "+_('career-content-2'), 200),
        'meta_kw': _('meta-kw-home'),
        'meta_img': request.build_absolute_uri(static('images/pcj-logo-og.jpg')),
        'meta_robots': 'index, nofollow',
    })
