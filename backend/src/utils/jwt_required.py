import functools
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import AccessToken
from utils.response import api_response

def jwt_required(view_func):
    @functools.wraps(view_func)
    def _wrapped_view(self, request: Request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return api_response(code=401, message='未登录或Token无效', data=None, status_code=401)
        token_str = auth_header.split(' ')[1]
        try:
            token = AccessToken(token_str)
            user_id = token['user_id']
            # 注入 user_id 到 request
            request.user_id = user_id
        except Exception:
            return api_response(code=401, message='Token无效或已过期', data=None, status_code=401)
        return view_func(self, request, *args, **kwargs)
    return _wrapped_view
