from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from settings import MEDIA_ROOT
import services.views

urlpatterns = patterns('services.views',
    # Examples:
    # url(r'^$', 'kisan_net.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', 'register'),
    url(r'^queue/$', 'queue_reg'),
    url(r'^asklabour/$', 'asklabour'),
    url(r'^listlabour/$', 'listlabour'),
    url(r'^editlabour/$', 'editlabour'),
    url(r'^post_put/$', 'post_put_request'),
    url(r'^post_get/$', 'post_get_request'),
    url(r'^fetch_put/(\d+)/$', 'fetch_put_requests'),
    url(r'^fetch_put/$', 'fetch_put_requests'),
    url(r'^fetch_get/(\d+)/$', 'fetch_get_requests'),
    url(r'^fetch_get/$', 'fetch_get_requests'),
    url(r'^del/$', 'del_debug'),

)+static(MEDIA_ROOT, document_root=MEDIA_ROOT)
