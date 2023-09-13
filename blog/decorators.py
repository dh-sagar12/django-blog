from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from blog.models import Author


def author_can_access(view_function):

    def _inner_func(request, *args, **kwargs):
        try:
            author = get_object_or_404(
                Author, is_verified=True, id=request.user.id)
            if author.id  ==  request.user.id:
                return view_function(request, *args, **kwargs) 

        except Exception as e:
            return HttpResponseForbidden("Forbidden Page.")
        
    return _inner_func