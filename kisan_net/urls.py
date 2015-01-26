from django.conf.urls import patterns, include, url
from django.contrib import admin
import services.views

urlpatterns = patterns('services.views',
    # Examples:
    # url(r'^$', 'kisan_net.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', 'register'),
    url(r'^queue/$', 'queue_reg'),
    url(r'^asklabour/$', 'asklabour'),
    url(r'^del/$', 'del_debug'),

)
