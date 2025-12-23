from django.db import connection
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from utils.response import api_response

class SimpleUser:
    """一个简单的用户对象，用于生成Token"""
    def __init__(self, user_id):
        self.pk = user_id
        self.id = user_id

def get_user_id_from_token(request):
    """从请求头中手动解析 Token 获取 user_id"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token_str = auth_header.split(' ')[1]
    try:
        token = AccessToken(token_str)
        return token['user_id']
    except Exception:
        return None

class LoginView(APIView):
    """
    自定义登录视图：完全使用 SQL 查询 user 表
    """
    permission_classes = [] # 允许匿名访问

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return api_response(code=1, message='用户名和密码不能为空')

        user_id = None
        db_password = None

        # 查询用户
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, password FROM users WHERE username = %s", [username])
            row = cursor.fetchone()
            if row:
                user_id = row[0]
                db_password = row[1]
        
        # 验证密码
        if not user_id or not check_password(password, db_password):
            return api_response(code=2, message='用户名或密码错误')

        # 检查是否为创作者
        role = 'user'
        artist_id = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM user_become_artist WHERE user_id=%s", [user_id])
            row = cursor.fetchone()
            if row:
                role = 'artist'
                artist_id = row[0]

        # 手动生成JWT Token
        user_obj = SimpleUser(user_id)
        refresh = RefreshToken.for_user(user_obj)

        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': role,
            'user_id': user_id,
            'artist_id': artist_id,
        }
        return api_response(code=0, message='登录成功', data=data)


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                return api_response(code=1, message='用户名和密码不能为空')

            with connection.cursor() as cursor:
                # 允许重名
                # 密码加密
                hashed_password = make_password(password)
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    [username, hashed_password]
                )
                
            return api_response(code=0, message='注册成功', data={
                'username': username,
                'password': password
            })
        except Exception as e:
            return api_response(code=2, message='注册失败: ' + str(e))


class MeView(APIView):
    permission_classes = []

    def get(self, request):
        user_id = get_user_id_from_token(request)
        if not user_id:
            return api_response(code=401, message='未登录或Token无效')

        username = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT username FROM users WHERE user_id = %s", [user_id])
            row = cursor.fetchone()
            if row:
                username = row[0]
        
        if not username:
            return api_response(code=404, message='用户不存在')

        role = 'user'
        artist_id = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM user_become_artist WHERE user_id=%s", [user_id])
            row = cursor.fetchone()
            if row:
                role = 'artist'
                artist_id = row[0]

        return api_response(data={
            'user_id': user_id,
            'username': username,
            'role': role,
            'artist_id': artist_id
        })

    def put(self, request):
        user_id = get_user_id_from_token(request)
        if not user_id:
            return api_response(code=401, message='未登录')
            
        new_username = request.data.get('username')
        if not new_username:
            return api_response(code=1, message='缺少用户名')
            
        with connection.cursor() as cursor:                
            cursor.execute("UPDATE users SET username = %s WHERE user_id = %s", [new_username, user_id])
            
        return api_response(message='用户名修改成功')


class ChangePasswordView(APIView):
    permission_classes = []

    def post(self, request):
        user_id = get_user_id_from_token(request)
        if not user_id:
            return api_response(code=401, message='未登录')

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return api_response(code=1, message='参数不完整')

        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM users WHERE user_id = %s", [user_id])
            row = cursor.fetchone()
            if not row:
                return api_response(code=404, message='用户不存在')
            
            db_password = row[0]

            if not check_password(old_password, db_password):
                return api_response(code=2, message='旧密码错误')

            new_hashed = make_password(new_password)
            cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", [new_hashed, user_id])

        return api_response(message='密码修改成功')


class LogoutView(APIView):
    permission_classes = []
    def post(self, request):
        return Response({"code": 0, "message": "已注销"})