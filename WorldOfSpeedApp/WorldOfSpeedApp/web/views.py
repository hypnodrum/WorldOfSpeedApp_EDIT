from django.shortcuts import render


def index(request):
    logged_in_user = request.user

    if logged_in_user.is_authenticated:
        return render(request, "web/index.html", {'user': logged_in_user})
    else:
        return render(request, "web/index-no-profile.html")
