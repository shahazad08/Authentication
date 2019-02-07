
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
admin.autodiscover()
# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # for a home page
    # url(r'^register/',include('users.urls')),
    # url(r'^register1/', include('users.urls')),
    # url(r'^$', 'home', name='home'),
    path('admin/', admin.site.urls),    # for a admin login
    url(r'^user/', include(('users.urls','users'),namespace='users')),  # create model
    url(r'^temail/',include('users.urls')),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # url('^', include('django.cont
    # rib.auth.urls')),
]

# urlpatterns=format_suffix_patterns(urlpatterns)
