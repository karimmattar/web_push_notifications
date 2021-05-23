# views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View


class HomeView(View):
    template_name = "home.html"

    @method_decorator(login_required)
    def get(self, request):
        group_name = 'group_%s' % request.user.get_username()
        notifications = request.user.notifications.all()
        count = notifications.filter(is_seen=False).count()
        print(group_name, )
        return render(request, self.template_name, {
            'group_name': group_name, 'notifications': notifications, 'count': count
        })

