from datetime import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import CustomUser, CustomUserStatus


# birthdate validation basic requirement
def in_past_years_restriction(birthdate):
    if birthdate.year >= datetime.today().year:
        raise serializers.ValidationError(_("entered Birth Date must be in the Past."))
    return birthdate


class CustomUserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    birthdate = serializers.DateField(label='Date of Birth', validators=[in_past_years_restriction])

    class Meta:
        model = CustomUser
        fields = [
            "id", "first_name", "last_name", "country_code", "phone_number", "gender", "birthdate",
            "avatar", "email"
        ]


class CustomUserSetPasswordSerializer(serializers.Serializer):
    model = CustomUser
    phone_number = serializers.CharField(label='Phone Number', max_length=12, validators=[CustomUser.PHONE_REGEX])
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def create(self, validated_data):
        user = CustomUser.objects.get(phone_number=validated_data.get('phone_number'))
        if user and validated_data.get('new_password1') == validated_data.get('new_password2'):
            # directly set the user's empty password
            user.set_password(validated_data.get('new_password2'))
            user.save()
            return user
        return None


class CustomUserStatusSerializer(serializers.Serializer):
    model = CustomUserStatus
    phone_number = serializers.CharField(label='Phone Number', max_length=12, validators=[CustomUser.PHONE_REGEX])
    auth_token = serializers.CharField(label='Auth-Token', required=True)
    status = serializers.JSONField(label='Status', required=True)

    def create(self, validated_data, request):
        try:
            user = CustomUser.objects.get(phone_number=validated_data.get('phone_number'))
        except CustomUser.DoesNotExist:
            return None
        if user and request.user == user:
            import json
            status = json.loads(validated_data.get('status').replace("'", '"'))
            return CustomUserStatus.objects.create(
                user=user, status=status,
                phone_number=validated_data.get('phone_number'),
                auth_token=validated_data.get('auth_token'),
            )
        return None
