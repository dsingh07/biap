from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# List of URLs used and accessed by views
# app1.views shortcut appends onto second view argument
# model parameter patient_id also used in urls

urlpatterns = patterns('app1.views',
    url(r'^$', 'home'),
    url(r'^index/$', 'index'),
    url(r'^overview/$', 'overview'),
    url(r'^index/(?P<patient_id>\d+)/$', 'detail'),
    url(r'^get_data/$', 'webhook'),
    url(r'^index/(?P<patient_id>\d+)/patient_data/$', 'patient_data'),
    url(r'^index/(?P<patient_id>\d+)/raw_data/$', 'raw_data'),
    url(r'^index/(?P<patient_id>\d+)/csv/$', 'csv_export'),
    url(r'^register/$', 'register'),
    url(r'^login/$', 'user_login'),
    url(r'^logout/$', 'user_logout'),
)

# administration page URL
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)