from django.shortcuts import redirect
from django.http import HttpResponse

def allowed_user(allow_rolls=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allow_rolls:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not allowed to view this page')
        return wrapper
    return decorator