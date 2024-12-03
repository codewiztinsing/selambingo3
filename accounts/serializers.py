from accounts.models import TelegramUser
from rest_framework import serializers
class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, label='Confirm Password')

    def create(self, validated_data):
        # Remove m2m fields from validated_data
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        password = validated_data.pop('password')
        password_confirm = validated_data.pop('password_confirm', None)

        # Create user instance
        user = TelegramUser(**validated_data)
        user.set_password(password)
        user.save()

        # Set m2m fields after user is created
        if groups is not None:
            user.groups.set(groups)
        if user_permissions is not None:
            user.user_permissions.set(user_permissions)

        return user

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords don't match")
        return data

    class Meta:
        model = TelegramUser
        fields = [
            'id', 'username', 'password', 'password_confirm', 'telegram_id',
            'first_name', 'last_name', 'telegram_username', 'language_code',
            'is_bot', 'created_at', 'updated_at', 'groups', 'user_permissions',
            'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined',
            'phone'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']