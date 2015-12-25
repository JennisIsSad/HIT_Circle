from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

#from django.conf.urls import *
#from addr_book.views import hello, current_time
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_PATH}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/hot/\S*','addr_book.views.home_hot'),
    url(r'^home/latest/\S*','addr_book.views.home_latest'),
    url(r'^home/friends/\S*','addr_book.views.home_friends'),
    url(r'^home/invitation/unchecked','addr_book.views.invitation'),
    url(r'^home/invitation/checked','addr_book.views.invitation2'),
    url(r'^home/invitation/sent','addr_book.views.invitation3'),
    url(r'^home/message/unread','addr_book.views.message_unread'),
    url(r'^home/message/read','addr_book.views.message_read'),
    url(r'^home/message/replid','addr_book.views.message_replid'),
    url(r'^profile/','addr_book.views.profile'),
    url(r'^userinfo_update/','addr_book.views.userinfo_update'),
    url(r'^reject/','addr_book.views.reject'),
    url(r'^accept/','addr_book.views.accept'),
    url(r'^registration/','addr_book.views.registration'),
    url(r'^login','addr_book.views.user_login'),
    url(r'^add_friend/','addr_book.views.add_friend'),
    url(r'^remove_friend/','addr_book.views.remove_friend'),
    url(r'^delete_tweet/','addr_book.views.delete_tweet'),
    url(r'^logout/','addr_book.views.logout_ok'),
    url(r'^mypassword/','addr_book.views.set_password'),
    )
