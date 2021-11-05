from functools import wraps

from rest_framework.response import Response

from token_receiver.models import PostToken


def is_logged_in(fn):
    def wrapper(request, *args, **kwargs):
        if args[0].session.get('name') is None:
            return Response({'error': 'you not logged in'}, status=400)
        kwargs['key'] = args[0].session.get('name')
        return fn(request, *args, **kwargs)

    return wrapper


def is_not_logged_in(fn):
    def wrapper(request, *args, **kwargs):
        if args[0].session.get('name') is not None:
            return Response({'error': 'you already logged in'}, status=400)
        kwargs['key'] = args[0].session.get('name')
        return fn(request, *args, **kwargs)

    return wrapper


def is_not_token_valid(fn):
    def wrapper(request, *args, **kwargs):
        if args[0].token is not None:
            if args[0].token == 'Not passed':
                return Response({'error': 'Token is not passed'}, status=400)
            if args[0].token == 'Need update':
                return Response({'error': 'Update token'}, status=400)
            return fn(request, *args, **kwargs)

        else:
            return Response({'error': 'Token is not valid'}, status=400)
    return wrapper