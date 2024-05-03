from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic.edit import FormView

from .forms import AddressForm, CustomPasswordChangeForm, UserForm, UserRegistrationForm, UserLoginForm
from .models import Address, User


class RegisterAndLoginView(View):
    templates_name = 'login-register.html'

    def get(self, request):
        context = {
            'register_form': UserRegistrationForm(),
            'login_form': UserLoginForm()
        }
        return render(request, self.templates_name, context)

    def post(self, request):
        register_form = UserRegistrationForm(request.POST)
        login_form = UserLoginForm(request.POST)

        if 'register' in request.POST:
            if register_form.is_valid():
                register_form.save()
                return redirect('index')
        elif 'login' in request.POST:
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')

        context = {
            'register_form': register_form,
            'login_form': login_form,
        }
        return render(request, 'login-register.html', context)


class ProfileView(LoginRequiredMixin, FormView):
    form_class = UserForm
    template_name = 'account/account.html'
    success_url = reverse_lazy('address')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.user = User.objects.get(email=self.request.user)
        kwargs['instance'] = self.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid()


class AddressView(FormView):
    form_class = AddressForm
    template_name = 'account/address.html'
    success_url = reverse_lazy('address')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            self.address = Address.objects.get(user=self.request.user)
        except Address.DoesNotExist:
            self.address = None
        kwargs['instance'] = self.address
        return kwargs

    def form_valid(self, form):
        if not self.address:
            self.address = form.save(commit=False)
            self.address.user = self.request.user
            self.address.save()
        else:
            form.save()
        return super().form_valid(form)


class ChangePasswordView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')
