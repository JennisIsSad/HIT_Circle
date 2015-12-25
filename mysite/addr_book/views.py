#from django.shortcuts import render
from django.template import Context
from django.shortcuts import render_to_response
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from addr_book.models import Tweet, Friendship, FriendshipInvitation, Comment, Notition
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
class Tweets(object):
    def __init__(self, tweet):
        self.tweet = tweet
        self.comments = []
        self.com_num = 0
        self.isf = False

def home_hot(request):
    '''##'''
    pageItemNum = 3
    current_page = 0
    '''##'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    user_ = request.user
    if request.POST:
        if request.POST.has_key("inputbox"):
            tweet_con = request.POST["inputbox"]
            new_tweet = Tweet(
                user = user_,
                content = tweet_con
            )
            new_tweet.save()
        if request.POST.has_key("commentbox"):
            com_con = request.POST["commentbox"]
            tweet_id =  request.POST["id"]
            '''##'''
            current_page = int(request.POST['page'])
            '''##'''
            to_tweet = Tweet.objects.get(id = int(tweet_id))
            new_comment = Comment(
                user = user_,
                content = com_con,
                tweet = to_tweet
            )
            new_comment.save()
            new_notition = Notition(
                f_comm = new_comment,
                t_comm = new_comment,
                to_tweet = to_tweet,
                to_user = to_tweet.user,
                noti_type = "1",
                status = "1"
            )
            new_notition.save()
    if request.GET:
        if request.GET.has_key("search"):
            friends = []
            tweet_list = []
            for friendship in Friendship.objects.filter(to_user = user_):
                friends.append(friendship.from_user)
            for friendship in Friendship.objects.filter(from_user = user_):
                friends.append(friendship.to_user)
            friend_num = len(friends)
            s_user = get_object_or_404(User, username = request.GET["search"])
            isf = Friendship.objects.are_friends(s_user, request.user)
            for tweet in Tweet.objects.filter(user = s_user):
                new_tweet = Tweets(tweet)
                new_tweet.comments = list(tweet.comment_set.all())
                new_tweet.com_num = tweet.comment_set.all().count()
                new_tweet.isf = isf
                tweet_list.append(new_tweet)
            tweet_list.sort(key=lambda x:(x.com_num, x.tweet.tweet_time), reverse = True)
            tweet_num = Tweet.objects.filter(user = user_).count()
            no_num = Notition.objects.filter(to_user = user_).filter(status = "1").count()
            '''##'''
            page_num = tweet_num/pageItemNum
            if request.GET.has_key('page'):
               current_page = int(request.GET['page'])
            '''##'''
            c = Context({"tweet_list": tweet_list[current_page*pageItemNum:(1 + current_page)*pageItemNum],\
            "friends" :friends, "current_user" : user_, \
            #
            'current_page': current_page,\
            'page_num': page_num,\
            #
            "friend_num":friend_num, "tweet_num":tweet_num, \
            "invitation_num":FriendshipInvitation.objects.filter\
            (to_user = request.user).filter( status = "1").count(),
            "notition_num": no_num})
            return render_to_response("home1.html", c)
        
    friends = []
    for friendship in Friendship.objects.filter(to_user = user_):
        friends.append(friendship.from_user)
    for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
    friend_num = len(friends)
    tweet_list = []
    for tweet in Tweet.objects.all():
        new_tweet = Tweets(tweet)
        new_tweet.comments = list(tweet.comment_set.all())
        new_tweet.com_num = tweet.comment_set.all().count()
        new_tweet.isf = Friendship.objects.are_friends(tweet.user, request.user)
        tweet_list.append(new_tweet)
    tweet_list.sort(key=lambda x:(x.com_num, x.tweet.tweet_time), reverse = True)
    tweet_num = Tweet.objects.filter(user = user_).count()
    no_num = Notition.objects.filter(to_user = user_).filter(status = "1").count()
    '''##'''
    page_num = tweet_num/pageItemNum
    if request.GET.has_key('page'):
       current_page = int(request.GET['page'])
    '''##'''
    c = Context({"tweet_list": tweet_list[current_page*pageItemNum:(1 + current_page)*pageItemNum],\
    "friends" :friends, "current_user" : user_, \
    #
    'current_page': current_page,\
    'page_num': page_num,\
    #
    "friend_num":friend_num, "tweet_num":tweet_num, \
    "invitation_num":FriendshipInvitation.objects.filter\
    (to_user = request.user).filter(status = "1").count(),
    "notition_num": no_num})
    return render_to_response("home1.html", c)


def home_latest(request):
    '''##'''
    pageItemNum = 3
    current_page = 0
    '''##'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    user_ = request.user
    if request.POST:
        if request.POST.has_key("inputbox"):
            tweet_con = request.POST["inputbox"]
            new_tweet = Tweet(
                user = user_,
                content = tweet_con
            )
            new_tweet.save()
        if request.POST.has_key("commentbox"):
            com_con = request.POST["commentbox"]
            tweet_id =  int(request.POST["id"])
            '''##'''
            current_page = int(request.POST['page'])
            '''##'''
            to_tweet = Tweet.objects.get(id = int(tweet_id))
            new_comment = Comment(
                user = user_,
                content = com_con,
                tweet = to_tweet
            )
            new_comment.save()
            new_notition = Notition(
                f_comm = new_comment,
                t_comm = new_comment,
                to_tweet = to_tweet,
                to_user = to_tweet.user,
                noti_type = "1",
                status = "1"
            )
            new_notition.save()
    if request.GET:
        if request.GET.has_key("search"):
            friends = []
            tweet_list = []
            for friendship in Friendship.objects.filter(to_user = user_):
                friends.append(friendship.from_user)
            for friendship in Friendship.objects.filter(from_user = user_):
                friends.append(friendship.to_user)
            friend_num = len(friends)
            s_user = get_object_or_404(User, username = request.GET["search"])
            for tweet in Tweet.objects.filter(user = s_user):
                new_tweet = Tweets(tweet)
                new_tweet.comments = list(tweet.comment_set.all())
                new_tweet.com_num = tweet.comment_set.all().count()
                new_tweet.isf = Friendship.objects.are_friends(tweet.user, request.user)
                tweet_list.append(new_tweet)
            tweet_list.sort(key=lambda x:x.tweet.tweet_time, reverse = True)
            tweet_num = Tweet.objects.filter(user = user_).count()
            no_num = Notition.objects.filter(to_user = user_).filter(status = "1").count()
            '''##'''
            page_num = tweet_num/pageItemNum
            if request.GET.has_key('page'):
               current_page = int(request.GET['page'])
            '''##'''
            c = Context({"tweet_list": tweet_list[current_page*pageItemNum:(1 + current_page)*pageItemNum],\
            "friends" :friends, "current_user" : user_, \
            #
            'current_page': current_page,\
            'page_num': page_num,\
            #
            "friend_num":friend_num, "tweet_num":tweet_num, \
            "invitation_num":FriendshipInvitation.objects.filter\
            (to_user = request.user).filter( status = "1").count(),
            "notition_num": no_num})
            return render_to_response("home2.html", c)
            
        
    friends = []
    for friendship in Friendship.objects.filter(to_user = user_):
        friends.append(friendship.from_user)
    for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
    friend_num = len(friends)
    tweet_list = []
    for tweet in Tweet.objects.all():
        new_tweet = Tweets(tweet)
        new_tweet.comments = list(tweet.comment_set.all())
        new_tweet.com_num = tweet.comment_set.all().count()
        new_tweet.isf = Friendship.objects.are_friends(tweet.user, request.user)
        tweet_list.append(new_tweet)
    tweet_list.sort(key=lambda x:x.tweet.tweet_time, reverse = True)
    tweet_num = Tweet.objects.filter(user = user_).count()
    '''##'''
    page_num = tweet_num/pageItemNum
    if request.GET.has_key('page'):
       current_page = int(request.GET['page'])
    '''##'''
    no_num = Notition.objects.filter(to_user = user_).filter(status = "1").count()
    c = Context({"tweet_list": tweet_list[current_page*pageItemNum:(1 + current_page)*pageItemNum],\
    "friends" :friends, "current_user" : user_, \
    #
    'current_page': current_page,\
    'page_num': page_num,\
    #
    "friend_num":friend_num, "tweet_num":tweet_num, \
    "invitation_num":FriendshipInvitation.objects.filter\
    (to_user = request.user).filter( status = "1").count(),
    "notition_num": no_num})
    return render_to_response("home2.html", c)

def home_friends(request):
    '''##'''
    pageItemNum = 3
    current_page = 0
    '''##'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    
    user_ = request.user
    if request.POST:
        if request.POST.has_key("inputbox"):
            tweet_con = request.POST["inputbox"]
            new_tweet = Tweet(
                user = user_,
                content = tweet_con
            )
            new_tweet.save()
        if request.POST.has_key("commentbox"):
            com_con = request.POST["commentbox"]
            tweet_id =  request.POST["id"]
            '''##'''
            current_page = int(request.POST['page'])
            '''##'''
            to_tweet = Tweet.objects.get(id = int(tweet_id))
            new_comment = Comment(
                user = user_,
                content = com_con,
                tweet = to_tweet
            )
            new_comment.save()
    if request.GET:
        if request.GET.has_key("search"):
            friends = []
            tweet_list = []
            for friendship in Friendship.objects.filter(to_user = user_):
                friends.append(friendship.from_user)
            for friendship in Friendship.objects.filter(from_user = user_):
                friends.append(friendship.to_user)
            friend_num = len(friends)
            s_user = get_object_or_404(User, username = request.GET["search"])
            for tweet in Tweet.objects.filter(user = s_user):
                new_tweet = Tweets(tweet)
                new_tweet.comments = list(tweet.comment_set.all())
                new_tweet.com_num = tweet.comment_set.all().count()
                new_tweet.isf = True
                tweet_list.append(new_tweet)
            tweet_list.sort(key=lambda x:x.tweet.tweet_time, reverse = True)
            tweet_num = Tweet.objects.filter(user = user_).count()
            '''##'''
            page_num = len(tweet_list)/pageItemNum
            if request.GET.has_key('page'):
               current_page = int(request.GET['page'])
            '''##'''
            no_num = Notition.objects.filter(to_user = user_).filter(status = "1").count()
            c = Context({"tweet_list": tweet_list[current_page*pageItemNum:(1 + current_page)*pageItemNum],\
            "friends" :friends, "current_user" : user_, \
            #
            'current_page': current_page,\
            'page_num': page_num,\
            #
            "friend_num":friend_num, "tweet_num":tweet_num, \
            "invitation_num":FriendshipInvitation.objects.filter\
            (to_user = request.user).filter( status = "1").count(),
            "notition_num": no_num})
            return render_to_response("home3.html", c)
        
    friends = []
    tmp_tweet_list = []
    tweet_list = []
    for friendship in Friendship.objects.filter(to_user = user_):
        friends.append(friendship.from_user)
        tmp_tweet_list.extend(friendship.from_user.tweet_set.all())
    for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
        tmp_tweet_list.extend(friendship.to_user.tweet_set.all())
        
    for tweet in tmp_tweet_list:
        new_tweet = Tweets(tweet)
        new_tweet.comments = list(tweet.comment_set.all())
        new_tweet.com_num = tweet.comment_set.all().count()
        new_tweet.isf = True
        tweet_list.append(new_tweet)
    tweet_list.sort(key=lambda x:x.tweet.tweet_time, reverse = True)
    tweet_num = Tweet.objects.filter(user = user_).count()
    no_num = Notition.objects.filter(to_user = user_).filter(status = "1").count()
    friend_num = len(friends)
    '''##'''
    page_num = len(tweet_list)/pageItemNum
    if request.GET.has_key('page'):
       current_page = int(request.GET['page'])
    '''##'''
    c = Context({"tweet_list": tweet_list[current_page*pageItemNum:(1 + current_page)*pageItemNum],\
    "friends" :friends, "current_user" : user_, \
    #
    'current_page': current_page,\
    'page_num': page_num,\
    #
    "friend_num":friend_num, "tweet_num":tweet_num,\
    "invitation_num":FriendshipInvitation.objects.filter\
    (to_user = request.user).filter( status = "1").count(),
    "notition_num": no_num})
    return render_to_response("home3.html", c)

def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    user1 =  get_object_or_404(User, username = request.GET["username"])
    user_ = request.user
    friends = []
    for friendship in Friendship.objects.filter(to_user = user_):
        friends.append(friendship.from_user)
    for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
    friend_num = len(friends)
    tweet_num = Tweet.objects.filter(user = user_).count()
    c = Context({"tweet_list": Tweet.objects.filter(user = user1), "friends" :friends, \
    "notition_num": Notition.objects.filter(to_user = user_).filter( status = "1").count(),
    "current_user" : user_, "friend_num":friend_num, "user1" : user1, "tweet_num":tweet_num,
    "invitation_num":FriendshipInvitation.objects.filter(to_user = request.user).filter( status = "1").count()})
    return render_to_response("profile.html", c)
    
def delete_tweet(request):
    id = request.GET["id"]
    tweet = Tweet.objects.get(id = int(id))
    tweet.delete()
    return render_to_response("delete_tweet.html")
    
def userinfo_update(request):
    current_user = request.user
    if request.POST:       
       current_user.realname = request.POST["realname"]
       current_user.email = request.POST["email"]
       tmp_sex = request.POST["sex"]
       current_user.profession = request.POST["profession"]
       if tmp_sex == "F":
          print tmp_sex
          current_user.sex = False
       else:
          print tmp_sex
          current_user.sex = True
       current_user.save()
       return render_to_response("update_ok.html",id)
    c = Context({"current_user": current_user})
    return render_to_response("userinfo.html", c)
    
def registration(request):
    right=""
    if request.POST:       
        n_username = request.POST["username"]  
        n_password = request.POST["password"]
        n_password_re = request.POST["password_re"]
        n_realname = request.POST["realname"]
        n_email = request.POST["email"]
        tmp_sex = request.POST["sex"]
        n_profession = request.POST["profession"]
       
        if n_password == n_password_re:
            try:
                new_user = User.objects.create_user(
                username = n_username,
                realname = n_realname,
                email = n_email,
                profession = n_profession,
                password = n_password)
                if tmp_sex == "F":
                    print tmp_sex
                    new_user.sex = False
                else:
                    print tmp_sex
                    new_user.sex = True
                new_user.save()
                new_user = auth.authenticate(username = n_username, password = n_password)
                auth.login(request, new_user)
                return HttpResponseRedirect("/home/hot/")
            except:
                right="This user has existed."
                return render_to_response("registration.html",{"right":right})
        else:
            right="Your passwords are different."
            return  render_to_response("registration.html",{"right":right})
    return render_to_response('registration.html')
    
def user_login(request):
    if request.POST:
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/home/hot/")
            else:
                return render_to_response('Error.html')
        else:
            return render_to_response('Error.html')
    return render_to_response('login.html')

def add_friend(request):
    new_friend =  get_object_or_404(User, username = request.GET["username"])
    if Friendship.objects.are_friends(request.user, new_friend):
        return render_to_response('have_been_friends.html')
    else:
        
        friendship_invitation = FriendshipInvitation(
            from_user = request.user,
            to_user = new_friend,
            status = "1"
        )
        friendship_invitation.save()
        return render_to_response('add_friend_ok.html')

def remove_friend(request):
    friend =  get_object_or_404(User, username = request.GET["username"])
    Friendship.objects.remove(request.user, friend)
    return render_to_response('remove_friend_ok.html')

def invitation(request):
     if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
     user_ = request.user
     friends = []
     for friendship in Friendship.objects.filter(to_user = user_):
         friends.append(friendship.from_user)
     for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
     friend_num = len(friends)
     tweet_num = Tweet.objects.filter(user = user_).count()
     invitations = list(FriendshipInvitation.objects.filter(to_user = user_).filter( status = "1"))
     invitations.sort(key=lambda x:x.sent, reverse = True)
     c = Context({"invitations": invitations,\
                 "notition_num": Notition.objects.filter(to_user = user_).filter( status = "1").count(),
                  "invitation_num":FriendshipInvitation.objects.filter(to_user = user_).filter( status = "1").count(),\
                  "friend_num":friend_num, "friends" :friends,"current_user" : user_,"tweet_num":tweet_num})
     return render_to_response("invitations.html", c)


def invitation2(request):
    
     if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
     user_ = request.user
     friends = []
     invitations = []
     for friendship in Friendship.objects.filter(to_user = user_):
         friends.append(friendship.from_user)
     for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
     friend_num = len(friends)
     tweet_num = Tweet.objects.filter(user = user_).count()
     for invitation in FriendshipInvitation.objects.filter(to_user = user_).filter( status = "2"):
         invitations.append(invitation)
     for invitation in FriendshipInvitation.objects.filter(to_user = user_).filter( status = "3"):
         invitations.append(invitation)
     invitations.sort(key=lambda x:x.sent, reverse = True)
     c = Context({"invitations":invitations,\
                 "notition_num": Notition.objects.filter(to_user = user_).filter( status = "1").count(),
                  "invitation_num":FriendshipInvitation.objects.filter(to_user = user_).filter( status = "1").count(),\
                  "friend_num":friend_num, "friends" :friends,"current_user" : user_,"tweet_num":tweet_num})
     return render_to_response("invitation2.html", c)
     
def invitation3(request):
     if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
     user_ = request.user
     friends = []
     for friendship in Friendship.objects.filter(to_user = user_):
         friends.append(friendship.from_user)
     for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
     friend_num = len(friends)
     tweet_num = Tweet.objects.filter(user = user_).count()
     invitations = list(FriendshipInvitation.objects.filter(from_user = user_))
     invitations.sort(key=lambda x:x.sent, reverse = True)
     c = Context({"invitations":invitations,\
                 "notition_num": Notition.objects.filter(to_user = user_).filter( status = "1").count(),
                  "invitation_num":FriendshipInvitation.objects.filter(to_user = user_).filter( status = "1").count(),\
                  "friend_num":friend_num, "friends" :friends,"current_user" : user_,"tweet_num":tweet_num})
     return render_to_response("invitation3.html", c)
     
def message_unread(request):
    
     if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
        
     user_ = request.user
     if request.POST:
         if request.POST.has_key("commentbox"):
            com_con = request.POST["commentbox"]
            no_id =  request.POST["no_id"]
            noti = Notition.objects.get(id = int(no_id))
            noti.status = "3"
            noti.save()
            new_comment = Comment(
                user = user_,
                content = com_con,
                tweet = noti.to_tweet
            )
            new_comment.save()
            new_notition = Notition(
                f_comm = new_comment,
                t_comm = noti.f_comm,
                to_tweet = noti.to_tweet,
                to_user = noti.f_comm.user,
                noti_type = "2",
                status = "1"
            )
            new_notition.save()
        
     user_ = request.user
     friends = []
     for friendship in Friendship.objects.filter(to_user = user_):
         friends.append(friendship.from_user)
     for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
     friend_num = len(friends)
     tweet_num = Tweet.objects.filter(user = user_).count()
     notitions = Notition.objects.filter(to_user = user_).filter( status = "1")
     for noti in notitions:
         noti.status = "2"
         noti.save()
     print "OK"
     c = Context({"notitions": notitions,\
                  "notition_num": 0,
                  "invitation_num":FriendshipInvitation.objects.filter(to_user = user_).filter( status = "1").count(),\
                  "friend_num":friend_num, "friends" :friends,"current_user" : user_,"tweet_num":tweet_num})
     return render_to_response("message.html", c)
     
def message_read(request):
    
     if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
        
     user_ = request.user
     if request.POST:
         if request.POST.has_key("commentbox"):
            com_con = request.POST["commentbox"]
            no_id =  request.POST["no_id"]
            noti = Notition.objects.get(id = int(no_id))
            noti.status = "3"
            noti.save()
            new_comment = Comment(
                user = user_,
                content = com_con,
                tweet = noti.to_tweet
            )
            new_comment.save()
            new_notition = Notition(
                f_comm = new_comment,
                t_comm = noti.f_comm,
                to_tweet = noti.to_tweet,
                to_user = noti.f_comm.user,
                noti_type = "2",
                status = "1"
            )
            new_notition.save()
        
     user_ = request.user
     friends = []
     for friendship in Friendship.objects.filter(to_user = user_):
         friends.append(friendship.from_user)
     for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
     friend_num = len(friends)
     tweet_num = Tweet.objects.filter(user = user_).count()
     notitions = Notition.objects.filter(to_user = user_).filter( status = "2")
     c = Context({"notitions": notitions,\
                  "notition_num": Notition.objects.filter(to_user = user_).filter( status = "1").count(),
                  "invitation_num":FriendshipInvitation.objects.filter(to_user = user_).filter( status = "1").count(),\
                  "friend_num":friend_num, "friends" :friends,"current_user" : user_,"tweet_num":tweet_num})
     return render_to_response("message_read.html", c)

def message_replid(request):
    
     if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
        
     user_ = request.user
     if request.POST:
         if request.POST.has_key("commentbox"):
            com_con = request.POST["commentbox"]
            no_id =  request.POST["tweet_id"]
            noti = Notition.objects.get(id = int(no_id))
            new_comment = Comment(
                user = user_,
                content = com_con,
                tweet = noti.to_tweet
            )
            new_comment.save()
            new_notition = Notition(
                f_comm = new_comment,
                t_comm = noti.f_comm,
                to_tweet = noti.to_tweet,
                to_user = noti.f_comm.user,
                noti_type = "2",
                status = "1"
            )
            new_notition.save()
        
     user_ = request.user
     friends = []
     for friendship in Friendship.objects.filter(to_user = user_):
         friends.append(friendship.from_user)
     for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
     friend_num = len(friends)
     tweet_num = Tweet.objects.filter(user = user_).count()
     notitions = Notition.objects.filter(to_user = user_).filter( status = "3")
     c = Context({"notitions": notitions,\
                  "notition_num": Notition.objects.filter(to_user = user_).filter( status = "1").count(),
                  "invitation_num":FriendshipInvitation.objects.filter(to_user = user_).filter( status = "1").count(),\
                  "friend_num":friend_num, "friends" :friends, "current_user" : user_,"tweet_num":tweet_num})
     return render_to_response("message_replid.html", c)

def reject(request):
    id = request.GET["id"]
    book_select = FriendshipInvitation.objects.get(id = int(id))
    print "rejected"
    book_select.decline()
    return render_to_response("reject.html",id)

def accept(request):
    id = request.GET["id"]
    book_select = FriendshipInvitation.objects.get(id = int(id))
    book_select.accept()
    return render_to_response("accept.html",id)

def set_password(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    right=""
    if request.POST:
        password = request.POST["password"]
        password1 = request.POST["password1"]
        if password == password1:
            user = User.objects.get(username=request.user.username)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect("/login/")
        else :
            right="Your passwords are different."
            return  render_to_response("mypassword.html",{"right":right})
    return render_to_response("mypassword.html")

def author_not_exist(request):
    return render_to_response('author_not_exist.html')
    
def add_author_ok(request):
    return render_to_response('add_author_ok.html')

def add_book_ok(request):
    return render_to_response('add_book_ok.html')
    
def logout_ok(request):
    logout(request)
    return render_to_response('logout.html')