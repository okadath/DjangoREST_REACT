from rest_framework import serializers
from .models import Post,Profile
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'author', 'title', 'body', 'created_at',)
        model = Post

class GetFullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','is_superuser','first_name', 'last_name')



#serializer de creacion de usuario POST
class UserSerializerWithToken(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    # def get_token(self, object):
    #     #obtiene el token al vuelo
    #     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    #     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    #     payload = jwt_payload_handler(object)
    #     token = jwt_encode_handler(payload)
    #     return token
    def create(self, validated_data):
        #crear usuario, los datos se le pasan desde las vistas 
        #con UserSerializerWithToken(data = user)
        user = User.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    class Meta:
        model = User
        fields = ('token', 'username', 'password', 'first_name',
        'last_name')      

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user.username', 'bio')

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()

        return instance 







 