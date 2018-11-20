# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, CreateView, UpdateView
from users.forms import UserProfileForm, SignUpForm, ProfileForm
from users.models import Profile, User
from bookmart.utils import rendermessage, render_access_denied_message
from bookmart.settings import BASE_DIR
import os
from . import forms


class ProfileUpdateView(UpdateView):
    template_name = 'users/profile.html'
    model = Profile
    form_class = UserProfileForm
    second_form_class = ProfileForm

    def form_valid(self, form, form2):
        user = self.get_object().user
        if form.is_valid() and form2.is_valid():
            form.save()
        return super(ProfileUpdateView, self).form_valid(form2)

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        self.request = request
        if self.request.user.is_authenticated(
        ) and self.request.user.id == int(kwargs['pk']):
            super(ProfileUpdateView, self).get(request, *args, **kwargs)
            user = User.objects.get(pk=pk)
            prfl = Profile.objects.get(pk=pk)

            # if the image was removed then show the default image
            #if not default_storage.exists(prfl.image.url):
            #    prfl.image.url = 'assets/img/user.png'

            form = self.form_class(instance=user)
            form2 = self.second_form_class(instance=prfl)
            return self.render_to_response(
                self.get_context_data(
                    object=self.object, form=form, form2=form2))

        return render_access_denied_message(request)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            user = User.objects.get(pk=pk)
            prfl = Profile.objects.get(pk=pk)
            user_form = self.form_class(instance=user, data=request.POST)
            profile_form = self.second_form_class(
                instance=prfl, data=request.POST, files=request.FILES)
            #assert False, profile_form
            self.form_valid(user_form, profile_form)
            return confirmation_page(request, pk)

        else:
            render_access_denied_message(request)

    def get_success_url(self):
        return '/'


def confirmation_page(request, user_id):
    return rendermessage(request, 'Profile', 'Profile updated succefully', '',
                         reverse('users:profile', args=[str(user_id)]),
                         'profile page')


@login_required
def changepassword(request, user_id):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        if "Cancel" in request.POST:
            return reverse('users:profile', args=[str(user_id)]),
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return rendermessage(request, 'Password Confirmation',
                                 'Password changed succefully', '',
                                 reverse('users:profile',
                                         args=[str(user_id)]), 'profile')

    return render(
        request,
        'users/changepassword.html',
        {'form': form,
         'user_name': User.objects.get(pk=user_id)})


class LogoutView(LoginRequiredMixin, FormView):
    form_class = forms.LogoutForm
    template_name = 'users/logout.html'

    def form_valid(self, form):
        logout(self.request)
        return HttpResponseRedirect(reverse('home'))


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = '/users/login/'
