from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'loginandreg/index.html')

def register(request):
    if request.method == "GET":
        messages.error(request, 'Nice try, log in or register.')
        return redirect('/')
    user = User.userManager.register(request.POST['firstname'], request.POST['lastname'], request.POST['email'], request.POST['password'], request.POST['passc'])
    if 'errors' in user:
        error = user['errors']
        for msg in error:
             messages.error(request, msg)
        return redirect('/')
    # if 'errors' in user:
    #     messages.error(request, 'Invalid email.')
    #     return redirect('/')
    # elif 'errors1' in user:
    #     messages.error(request, 'Email already exists, please log in.')
    #     return redirect('/')
    # elif 'errors2' in user:
    #     messages.error(request, 'Password must match.')
    #     return redirect('/')
    # elif 'errors3' in user:
    #     messages.error(request, 'Name must contain more than two characters.')
    #     return redirect('/')
    # elif 'errors4' in user:
    #     messages.error(request, 'Name must contain only alpha characters.')
    #     return redirect('/')
    # elif 'errors5' in user:
    #     messages.error(request, 'Password must be greater than 8 characters.')
    #     return redirect('/')
    else:
        messages.success(request, 'Successfully registered!')
        User.userManager.create(first_name= user['first_name'], last_name= user['last_name'], email = user['email'], password = user['password'])
        user = User.userManager.filter(email = user['email'])
        request.session['userid'] = user[0].id
    return redirect('/success')

def success(request):
    if 'userid' not in request.session:
        messages.error(request, 'Nice try, log in or register.')
        return redirect('/')
    context = {'user': User.userManager.all(), 'loggeduser': User.userManager.get(id=request.session['userid'])}
    #context = {'user': User.userManager.filter(id=id)}
    return render(request, 'loginandreg/success.html', context)

def login(request):
    if request.method == "GET":
        messages.error(request, 'Nice try, log in or register.')
        return redirect('/')
    user = User.userManager.login(request.POST['email'], request.POST['password'])
    if 'errors' in user:
        error = user['errors']
        for msg in error:
            messages.error(request, msg)
        return redirect('/')
    # if 'errors' in user:
    #     messages.success(request, 'Invalid email.')
    #     return redirect('/')
    # elif 'errors5' in user:
    #     messages.error(request, 'Invalid password.')
    #     return redirect('/')
    # elif 'errors6' in user:
    #     messages.error(request, 'Email does not exist, please register.')
    #     return redirect('/')
    else:
        messages.success(request, 'Successfully logged in!')
        user = User.userManager.filter(email = request.POST['email'])
        request.session['userid'] = user[0].id
        return redirect('/success')

def logout(request):
    if 'userid' not in request.session:
        return redirect('/')
    del request.session['userid']
    return redirect('/')

def delete(request, id):
    if 'userid' not in request.session:
        messages.error(request, 'Nice try, log in or register.')
        return redirect('/')
    User.userManager.filter(id=id).delete()
    return redirect('/logout')
        #
        # {% for users in loggeduser %}
        # First Name: {{users.first_name}}<br />
        # Last Name: {{users.last_name}}<br />
        # Email: {{users.email}}<br />
            # <form action="/delete/{{users.id}}" method="post">
            #   {% csrf_token %}
            #   <input type="submit" value="Delete User">
            # </form><br />
            # {% endfor %}
        # Created: {{users.created_at}}<br />
def any(request):
    messages.error(request, 'Nice try.')
    return redirect('/')
