#from django.shortcuts import render
from django.template import Context
from django.shortcuts import render_to_response
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from addr_book.models import Tweet, Friendship
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home_all(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    user_ = request.user
    if request.POST:
        tweet_con = request.POST["inputbox"]
        new_tweet = Tweet(
            user = user_,
            content = tweet_con
        )
        new_tweet.save()
    friends = []
    for friendship in Friendship.objects.filter(to_user = user_):
        friends.append(friendship.from_user)
    for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
    friend_num = len(friends)
    tweet_num = Tweet.objects.filter(user = user_).count()
    c = Context({"tweet_list": Tweet.objects.all(), "friends" :friends, "current_user" : user_, "friend_num":friend_num, "tweet_num":tweet_num})
    
    return render_to_response("home2.html", c)

def home_friends(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    
    user_ = request.user
    if request.POST:
        tweet_con = request.POST["inputbox"]
        new_tweet = Tweet(
            user = user_,
            content = tweet_con
        )
        new_tweet.save()
    friends = []
    tweet_list = []
    for friendship in Friendship.objects.filter(to_user = user_):
        friends.append(friendship.from_user)
        tweet_list.extend(friendship.from_user.tweet_set.all())
    for friendship in Friendship.objects.filter(from_user = user_):
        friends.append(friendship.to_user)
        tweet_list.extend(friendship.to_user.tweet_set.all())
    friend_num = len(friends)
    tweet_num = Tweet.objects.filter(user = user_).count()
    c = Context({"tweet_list": tweet_list, "friends" :friends, "current_user" : user_, "friend_num":friend_num, "tweet_num":tweet_num})
    
    return render_to_response("home3.html", c)

def delete_tweet(request):
    id = request.GET["id"]
    tweet = Tweet.objects.get(id = int(id))
    tweet.delete()
    return render_to_response("delete_tweet.html")
'''def add_author(request):
    right = ""
    if request.POST:       
        author_name = request.POST["author_name"]  
        author_age = request.POST["author_age"]
        author_country = request.POST["author_country"]
        length = Author.objects.filter(Name = author_name).count()
        if length == 0:
            authorID = length + 1
            Author.objects.create(AuthorID = authorID, Name = author_name, Age = author_age, Country = author_country)
            return HttpResponseRedirect("/add_author_ok/")
        else:
            right = "This author has allready existed."
            return render_to_response("add_author.html",{"right":right})
    return render_to_response('add_author.html')
def add_book(request):
    word = ""
    if request.POST:
        post = request.POST
        isbn = post["isbn"]
        title = post["title"]
        author_ = post["author_name"]
        publisher = post["publisher"]
        publishdate = post["publishdate"]
        price = post["price"]
        le = Book.objects.filter(ISBN = isbn).count()
        if le == 0:
            try:
                author = Author.objects.get(Name = author_)
                new_book = Book(
                    ISBN = isbn,
                    Title = title,
                    Author = author,
                    Publisher = publisher,
                    PublishDate = publishdate,
                    Price = price
                    )
                new_book.save()
                return HttpResponseRedirect("/add_book_ok/")
            except:
                return HttpResponseRedirect("/author_not_exist/")
        else:
            word = "this book has already existed, please check the ISBN code"
                
    return render_to_response('add_book.html',{"word":word})'''
    
def registration(request):
    right=""
    if request.POST:       
        n_username = request.POST["username"]  
        n_password = request.POST["password"]
        n_password_re = request.POST["password_re"]
        n_realname = request.POST["realname"]
        n_email = request.POST["email"]
        n_sex = True
        n_profession = request.POST["profession"]
        if n_password == n_password_re:
            #try:
                new_user = User.objects.create_user(
                username = n_username,
                realname = n_realname,
                email = n_email,
                sex = n_sex,
                profession = n_profession,
                password = n_password)  
                new_user.save()
                print "OK!"
                new_user = auth.authenticate(username = n_username, password = n_password)
                auth.login(request, new_user)
                return HttpResponseRedirect("/home/all/")
            #except:
                #right="This user has existed."
                #return render_to_response("registration.html",{"right":right})
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
                return HttpResponseRedirect("/home/all/")
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
        friendship = Friendship(
            to_user = request.user,
            from_user = new_friend
        )
        friendship.save()
        return render_to_response('add_friend_ok.html')

def remove_friend(request):
    friend =  get_object_or_404(User, username = request.GET["username"])
    Friendship.objects.remove(request.user, friend)
    return render_to_response('remove_friend_ok.html')
    
'''def add_book2(request):
    word = ""
    name = request.GET["authorname"]
    if request.POST:
        post = request.POST
        post = request.POST
        isbn = post["isbn"]
        title = post["title"]
        publisher = post["publisher"]
        publishdate = post["publishdate"]
        price = post["price"]
        le = Book.objects.filter(ISBN = isbn).count()
        if le == 0:
            try:
                author = Author.objects.get(Name = name)
                new_book = Book(
                        ISBN = isbn,
                        Title = title,
                        Author = author,
                        Publisher = publisher,
                        PublishDate = publishdate,
                        Price = price
                        )
                new_book.save()
                return HttpResponseRedirect("/add_book_ok/")
            except:
                return HttpResponseRedirect("/author_not_exist/")
        else:
            word = "this book has already existed, please check the ISBN code"
    return render_to_response('add_book2.html',{"name":name, "word":word})

def delete_book(request):
    id = request.GET["id"]
    book_select = Book.objects.get(id = int(id))
    book_select.delete()
    return render_to_response("delete_book.html",id)


def update_book(request):
    id = request.GET["id"]
    abook = Book.objects.get(id = int(id))
    if request.POST:
        post = request.POST
        try:
            author = Author.objects.get(Name = post["author_name"])
            new_ps = post["publisher"]
            new_psd = post["publishdate"]
            new_price = post["price"]
            abook.Author = author
            abook.Publisher = new_ps
            abook.PublishDate = new_psd
            abook.Price = new_price
            abook.save()
            return HttpResponseRedirect("/update_book_ok/")
        except:
            return HttpResponseRedirect("/add_author/")
    return render_to_response("update_book.html",Context({"book": abook, "id": id}))
def update_book_ok(request):
    return render_to_response('update_book_ok.html')'''


'''def search_book(request):
    author = Author.objects.get(Name = request.GET["authorname"])
    books = author.book_set.all()
    word = "You can also add books of this author by clicking the Add button below"
    if len(books) == 0:
        word = "The works of this author maynot be include in our database, you can add one by clicking Add below"
    c = Context({"books":books, "author":author, "word":word})
    return render_to_response('index.html',c)'''
    
def author_not_exist(request):
    return render_to_response('author_not_exist.html')
    
def add_author_ok(request):
    return render_to_response('add_author_ok.html')

def add_book_ok(request):
    return render_to_response('add_book_ok.html')
    
def logout_ok(request):
    logout(request)
    return render_to_response('logout.html')