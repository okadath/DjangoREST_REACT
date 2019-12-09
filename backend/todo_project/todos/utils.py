from todos.serializers import GetFullUserSerializer

def custom_jwt_response_handler(token, request=None):
    return {
        'token' : token,
        # 'user' : GetFullUserSerializer(user, context={'request' : request}).data
    }