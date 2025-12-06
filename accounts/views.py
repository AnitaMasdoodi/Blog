from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ProfileEditForm
from .models import Profile

    

class ProfileView(View):
    temp = "account/profile.html"
    form_class = ProfileEditForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        profile = request.user.profile
        form = self.form_class(instance=profile)
        return render(request, self.temp, {"form": form, "profile": profile})
    

class ProfileEditView(View):
    temp = 'account/profile-edit.html'
    form_class = ProfileEditForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        profile = request.user.profile
        form = self.form_class(instance=profile)
        return render(request, self.temp, {'form': form, 'profile': profile}) 

    def post(self, request):
        profile = request.user.profile
        form = self.form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # profile.refresh_from_db()
            messages.success(request, "Profile successfully updated")
            return redirect("profile")
        return render(request, self.temp, {"form": form, "profile": profile})
    


from django.core.mail import send_mail

def send_test_email():
    send_mail(
        'Hello from Django',  # موضوع ایمیل
        'This is a test email sent from Django using SMTP.',  # متن ایمیل
        'your_email@gmail.com',  # فرستنده
        ['receiver_email@example.com'],  # گیرنده (می‌تواند لیست باشد)
        fail_silently=False,
    )


class ProfileDeleteView(View):
    temp = 'account/profile-delete.html'

    def setup(self, request, *args, **kwargs):
        self.profile_instance = request.user.profile
        return super().setup(request, *args, **kwargs)
    

    def get(self, request):
        return render(request, self.temp, {'profile':self.profile_instance})

    def post(self, request):
        self.profile_instance.user.is_active = False
        self.profile_instance.user.save()
        return redirect('home')
