from django.http import HttpResponseForbidden
from django.shortcuts import render


def user_owner_required(Cls):
    class View(Cls):
        def __init__(self, *args, **kwargs):
            super(*args, **kwargs)
            self.get = self.test_user_owner
            self.post = self.test_user_owner

        def test_user_owner(self, *args, **kwargs):
                if not self.get_object().created_by == self.request.user:
                    return HttpResponseForbidden(render(self.request, "forbidden.html", {}))
                else:
                    method = self.request.method.lower()
                    return getattr(super(), method)(*args, **kwargs)

    return View