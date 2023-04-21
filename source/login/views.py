from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import LoginForm


def login(request):
    login_form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            if login_form.cleaned_data['username'] == 'test' \
                and login_form.cleaned_data['password'] == '1234':

                return HttpResponseRedirect('/account')

    return render(request, 'login/login.html', {'login_form': login_form})

# class LoginFormView(FormView):
#     template_name = 'login/login.html'
#     form_class = LoginForm
#     # success_url = 'login/login.html'
# 
#     def form_valid(self, form):
#         # if form.cleaned_data['username'] == 'test' \
#         #     and form.cleaned_data['password'] == '1234':
#         # 
#         #     return HttpResponseRedirect('/account')
# 
#         # return render(request, 'login/login.html', {'login_form': form})
#         return super().form_valid(form)
#         # return HttpResponse('Hello')
