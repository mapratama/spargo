from django.conf.urls import patterns, url

from .views import (Login, Register, Logout, NotificationUpdate,
                    ChangePassword, PasswordReset)


urlpatterns = patterns('',
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^register$', Register.as_view(), name='register'),
    url(r'^notification-update$', NotificationUpdate.as_view(), name='notification_update'),
    url(r'^logout$', Logout.as_view(), name='logout'),
    url(r'^change-password$', ChangePassword.as_view(), name='change_password'),
    url(r'^password-reset$', PasswordReset.as_view(), name='password_reset'),
)
