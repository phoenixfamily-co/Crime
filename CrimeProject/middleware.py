from django.shortcuts import redirect
from django_user_agents.utils import get_user_agent


class MobileOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = get_user_agent(request)
        if not user_agent.is_mobile:
            return redirect('home:support-view')
        return self.get_response(request)
