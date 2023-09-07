from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# Create your views here.
from django.contrib.auth import get_user_model
from django.http import JsonResponse

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('posts:index')
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)

def profile(request, username):
    User = get_user_model()
    user_info = User.objects.get(username=username)
    context = {
        'user_info': user_info,
    }
    return render(request, 'accounts/profile.html', context)



def follow(request, username):
    
    User = get_user_model() 

    me = request.user
    you = User.objects.get(username=username) 

    if you in me.followings.all() :
        me.followings.remove(you)
    else:
        me.followings.add(you)

    return redirect('accounts:profile', username=username)

def logout(request):
    auth_logout(request)

    return redirect('accounts:login')
    
    
# def followers(request, username):
#     User = get_user_model()

#     person = User.objects.get(username=username)

#     context = {
#         'person': person,
#     }
#     return render(request,'accounts/followerlist.html', context)

# def followings(request, username):
#     User = get_user_model()
#     person = User.objects.get(username=username)

#     context = {
#         'person': person,
#     }
#     return render(request,'accounts/followings.html', context)


def follow_async(request, user_id, pfuser_id):
    # context = {
    #     'message': post_id,
    # }
    User = get_user_model()
    user = request.user
    pfuser = User.objects.get(id=pfuser_id)

    if pfuser in user.followings.all():
        user.followings.remove(pfuser)
        status = False # 팔로우 취소
        
    else:
        user.followings.add(pfuser)
        status = True # 팔로우 실행
        

    context = {
        'status': status,
        'count': len(pfuser.followers.all()),
        
        
    }
    
    return JsonResponse(context) # 문서를 return 하지 않고 그 데이터만 return 함.

