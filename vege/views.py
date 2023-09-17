from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def recipes(request):
    if request.method == 'POST':
        data = request.POST

        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            recipe_image=recipe_image
        )
        return redirect('/recipes/')
        print(data)

    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(
            recipe_name__icontains=request.GET.get('search'))
    context = {'recipes': queryset}

    return render(request, 'recipes.html', context)


def delete_recipe(request, id):
    print('id: ', id)
    queryset = Recipe.objects.get(id=id)
    queryset.delete()

    return redirect('/recipes/')


def update_recipe(request, id):
    print('id: ', id)
    queryset = Recipe.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        return redirect('/recipes/')

    context = {'recipe': queryset}
    return render(request, 'update_recipe.html', context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('password: ', password)

        if not User.objects.filter(username=username).exists():
            print('User.objects.filter(username=username).exists(): ',
                  User.objects.filter(username=username).exists())
            messages.info(request, "Username does not exist")
            return redirect('/login/')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid Password ")
            return render('/login/')
        else:
            login(request, user)
            print('login: ', login)
            return redirect('/recipes/')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/')


def sign_up(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()

    return render(request, 'register.html')
