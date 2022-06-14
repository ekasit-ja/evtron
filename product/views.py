from django.shortcuts import render
from django.utils.translation import gettext as _
from django.template.defaultfilters import striptags, truncatechars
from django.templatetags.static import static

# Create your views here.
def product_wind(request):
    return render(request, 'product/wind.html' , {
        'meta_title': _('pcj-industries-long'),
        'meta_desc': _('meta-desc-home'),
        'meta_kw': _('meta-kw-home'),
        'meta_img': request.build_absolute_uri(static('images/pcj-logo-og.jpg')),
        'meta_robots': 'index, follow',
    })

def product_move(request):
    return render(request, 'product/move.html' , {
        'meta_title': _('pcj-industries-long'),
        'meta_desc': _('meta-desc-home'),
        'meta_kw': _('meta-kw-home'),
        'meta_img': request.build_absolute_uri(static('images/pcj-logo-og.jpg')),
        'meta_robots': 'index, follow',
    })

def product_carry(request):
    return render(request, 'product/carry.html' , {
        'meta_title': _('pcj-industries-long'),
        'meta_desc': _('meta-desc-home'),
        'meta_kw': _('meta-kw-home'),
        'meta_img': request.build_absolute_uri(static('images/pcj-logo-og.jpg')),
        'meta_robots': 'index, follow',
    })

def product_max(request):
    return render(request, 'product/max.html' , {
        'meta_title': _('pcj-industries-long'),
        'meta_desc': _('meta-desc-home'),
        'meta_kw': _('meta-kw-home'),
        'meta_img': request.build_absolute_uri(static('images/pcj-logo-og.jpg')),
        'meta_robots': 'index, follow',
    })

def product_flash(request):
    return render(request, 'product/flash.html' , {
        'meta_title': _('pcj-industries-long'),
        'meta_desc': _('meta-desc-home'),
        'meta_kw': _('meta-kw-home'),
        'meta_img': request.build_absolute_uri(static('images/pcj-logo-og.jpg')),
        'meta_robots': 'index, follow',
    })
