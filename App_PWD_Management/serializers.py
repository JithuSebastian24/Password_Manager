from rest_framework import serializers
from .models import User,UserPassword

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
             instance.set_password(password)
        instance.save()
        return instance

class UserCreatePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPassword
        fields = ['id','cust','pwd']
        

    def to_representation(self, instance):
        self.fields['cust'] =  UserSerializer(read_only=True)
        return super(UserCreatePasswordSerializer, self).to_representation(instance)

class UserGetPasswordSerializer(serializers.ModelSerializer):
    user = UserCreatePasswordSerializer

    class Meta:
        model = UserPassword
        fields = ('__all__')


        
        
       
