from rest_framework import serializers
from my_app.models import User
from my_app.utils import Util
from django.utils.encoding import smart_str, force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import re


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password', }, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    @staticmethod
    def validate(attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        special = ["@", "#", "$", "%", "&", "^", "!", "+", "_"]
        if not len(password) >= 8:
            raise serializers.ValidationError("length should be at-least 8 digit")
        if not len(password) <= 16:
            raise serializers.ValidationError("length should not be greater than 16")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password should have at-least one digit")
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("Password should have at-least ine uppercase")
        if not any(char.islower() for char in password):
            raise serializers.ValidationError("Password should have at-least ine lowercase")
        if not any(char in special for char in password):
            raise serializers.ValidationError("Password should have at-least in special character ")
        if not len(username) >= 10:
            raise serializers.ValidationError("length of username field should have at-least 10")
        if not len(username) <= 12:
            raise serializers.ValidationError("length of username field should not be greater than 12")
        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm passwords doesn't match")
        return attrs

    @staticmethod
    def create(validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)
    #username = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['email', "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']


class SendResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ['email']

    @staticmethod
    def validate(attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("encoded UID", uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Reset password token", token)
            link = 'http://localhost:8000/reset/' + uid + '/' + token
            print("Reset Password Link ", link)
            # send email
            """body = 'CLick Following Link to Reset Your Password' + link
            data = {
                'subject': "Reset Your Password",
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)"""
            return attrs
        else:
            raise serializers.ValidationError("You are not Registered User")


class UserResetPasswordSerializer(serializers.Serializer):
    confirm_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uid = self.context.get('uid')
            token = self.context.get('token')
            special = ["@", "#", "$", "%", "&", "^", "!"]
            if not len(password) >= 8:
                raise serializers.ValidationError("length should be at-least 8 digit")
            if not len(password) <= 16:
                raise serializers.ValidationError("length should not be greater than 16")
            if not any(char.isdigit() for char in password):
                raise serializers.ValidationError("Password should have at-least one digit")
            if not any(char.isupper() for char in password):
                raise serializers.ValidationError("Password should have at-least ine uppercase")
            if not any(char.islower() for char in password):
                raise serializers.ValidationError("Password should have at-least ine lowercase")
            if not any(char in special for char in password):
                raise serializers.ValidationError("Password should have at-least in special character ")

            if password != confirm_password:
                raise serializers.ValidationError("Both passwords doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is invalid or expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifiers:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is invalid or expired")
