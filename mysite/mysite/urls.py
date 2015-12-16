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
    url(r'^home/all/','addr_book.views.home_all'),
    url(r'^home/friends/','addr_book.views.home_friends'),
    url(r'^registration/','addr_book.views.registration'),
    url(r'^login','addr_book.views.user_login'),
    url(r'^add_friend/','addr_book.views.add_friend'),
    url(r'^remove_friend/','addr_book.views.remove_friend'),
    url(r'^delete_tweet/','addr_book.views.delete_tweet'),
    url(r'^logout/','addr_book.views.logout_ok'),
    url(r'^update_book/','addr_book.views.update_book'),
    url(r'^search_book/','addr_book.views.search_book'), 
    url(r'^add_author/','addr_book.views.add_author'),
    url(r'^add_book/','addr_book.views.add_book'),
    url(r'^add_book2/','addr_book.views.add_book2'),
    url(r'^creat_user_ok/','addr_book.views.creat_user_ok'),
    url(r'^add_author_ok/','addr_book.views.add_author_ok'),
    url(r'^add_book_ok/','addr_book.views.add_book_ok'),
    url(r'^update_book_ok/','addr_book.views.update_book_ok'),
    url(r'^author_not_exist/','addr_book.views.author_not_exist'),
    )
