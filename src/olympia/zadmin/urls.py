from django.conf.urls import include, url
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from olympia.accounts.utils import redirect_for_login
from olympia.addons.urls import ADDON_ID

from . import views


# Hijack the admin's login to use our pages.
def login(request):
    # If someone is already auth'd then they're getting directed to login()
    # because they don't have sufficient permissions.
    if request.user.is_authenticated:
        raise PermissionDenied
    else:
        return redirect_for_login(request)


admin.site.site_header = admin.site.index_title = 'AMO Administration'
admin.site.login = login


urlpatterns = [
    # AMO stuff.
    url(r'^$', views.index, name='zadmin.index'),
    url(r'^models$', lambda r: redirect('admin:index'), name='zadmin.home'),
    url(r'^addon/manage/%s/$' % ADDON_ID,
        views.addon_manage, name='zadmin.addon_manage'),
    url(r'^addon/recalc-hash/(?P<file_id>\d+)/', views.recalc_hash,
        name='zadmin.recalc_hash'),
    url(r'^env$', views.env, name='zadmin.env'),
    url(r'^settings', views.show_settings, name='zadmin.settings'),
    url(r'^fix-disabled', views.fix_disabled_file, name='zadmin.fix-disabled'),
    url(r'^email_preview/(?P<topic>.*)\.csv$',
        views.email_preview_csv, name='zadmin.email_preview_csv'),

    url(r'^file-upload/(?P<uuid>[0-9a-f]{32})/download$',
        views.download_file_upload, name='zadmin.download_file_upload'),

    url(r'^features$', views.features, name='zadmin.features'),
    url(r'^features/collections\.json$', views.collections_json,
        name='zadmin.collections_json'),
    url(r'^features/featured-collection$', views.featured_collection,
        name='zadmin.featured_collection'),

    url(r'^monthly-pick$', views.monthly_pick,
        name='zadmin.monthly_pick'),

    url(r'^elastic$', views.elastic, name='zadmin.elastic'),
    url(r'^mail$', views.mail, name='zadmin.mail'),
    url(r'^email-devs$', views.email_devs, name='zadmin.email_devs'),
    url(r'^addon-search$', views.addon_search, name='zadmin.addon-search'),

    # Site Event admin.
    url(r'^events/(?P<event_id>\d+)?$', views.site_events,
        name='zadmin.site_events'),
    url(r'^events/(?P<event_id>\d+)/delete$', views.delete_site_event,
        name='zadmin.site_events.delete'),

    # The Django admin.
    url(r'^models/', include(admin.site.urls)),
    url(r'^models/(?P<app_id>.+)/(?P<model_id>.+)/search\.json$',
        views.general_search, name='zadmin.search'),
]
