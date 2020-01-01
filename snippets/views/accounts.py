from django.shortcuts import render
from django.http import HttpResponseRedirect
from snippets.forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = SignupForm()

    template_name = 'accounts/signup.html'
    context = {'form': form}

    return render(request, template_name, context)
