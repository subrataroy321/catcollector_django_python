from django.shortcuts import render, redirect
from .models import Cat, CatToy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# create your views (these are like your controller actions here)
############## USER ###############

def login_view(request):
    if request.method == 'POST': ## it was a POST request so send the login data when submits
        # try to login the user in
        form = AuthenticationForm(request, request.POST)
        if(form.is_valid()):
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect('/user/'+u)
                else: 
                    return HttpResponse('The account has been disabled.')
            else:
                return HttpResponse('The username and/or the password is incorrect')
    else: # it was a GET request so send the empty login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/cats')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/user/'+str(user))
        else:
            return HttpResponse('<h2>Try Again</h2>')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

@login_required
def profile(request, username):
    user = User.objects.get(username= username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})


############## CATS #################

# django will make a create cat form for us
@method_decorator(login_required, name='dispatch')
class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    #success_url = '/cats/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/cats')

class CatUpdate(UpdateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']

    def form_valid(self, form): ## its a hook do not need to call
        self.object = form.save(commit= False) # don't post to the db until we say so
        self.object.save()
        return HttpResponseRedirect('/cats/'+str(self.object.pk))

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats'

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cats_show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    toys = CatToy.objects.all()
    return render(request, 'cats/show.html', {'cat': cat, 'toys': toys})

##############  CATTOYS  ################

def cattoys_index(request):
    cattoys = CatToy.objects.all()
    return render(request, 'cattoys/index.html', {'cattoys': cattoys})

def cattoys_show(request, cattoy_id):
    cattoy = CatToy.objects.get(id=cattoy_id)
    return render(request, 'cattoys/show.html', {'cattoy': cattoy})

class CatToyCreate(CreateView):
    model = CatToy
    fields = '__all__'
    success_url = '/cattoys'

class CatToyUpdate(UpdateView):
    model = CatToy
    fields = ['name', 'color']
    success_url = '/cattoys'

class CatToyDelete(DeleteView):
    model = CatToy
    success_url = '/cattoys'

def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).cattoys.add(toy_id)
    #return HttpResponseRedirect('/cats/'+str(cat_id))
    return redirect('cats_show', cat_id=cat_id) ## Alternative wat of doing redirect

def unassoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).cattoys.remove(toy_id)
    return HttpResponseRedirect('/cats/'+str(cat_id))

##############  DEFAULT  ################

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')



# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

# cats = [
#     Cat('Lolo', 'tabby', 'foul little demon', 3),
#     Cat('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
#     Cat('Raven', 'black tripod', '3 legged cat', 4)
# ]