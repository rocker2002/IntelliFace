from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Course, StudentImage, User, Camera, Class, StudentCourses
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import Teacher, Student
from django.db.models import Q
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        token['email'] = user.email
        token['is_active'] = user.is_active
        token['first_name'] = user.first_name
        token['is_teacher'] = user.is_teacher
        token['is_student'] = user.is_student
        token['last_name'] = user.last_name
        token['phone_number'] = user.phone_number

        return token

    # def validate(self, attrs):
    #     email = attrs.get("email")
    #     password = attrs.get("password")
    #
    #     try:
    #         user = User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         raise serializers.ValidationError("Invalid credentials or inactive account.")
    #
    #     print (user.is_active)
    #
    #     if not user.is_active:
    #         raise serializers.ValidationError("User account is inactive.")
    #
    #     if not user.check_password(password):
    #         raise serializers.ValidationError("Invalid credentials or inactive account.")
    #
    #         # At this point, the user is valid and password matches
    #     refresh = MyTokenObtainPairSerializer.get_token(user)
    #     return {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token),
    #     }

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        try:
            new_refresh = RefreshToken()
            new_refresh.set_jti()
            new_refresh.set_exp()
            new_refresh.set_iat()
            new_refresh.payload['user_id'] = refresh.payload['user_id']

            user_id = refresh.payload['user_id']
            user = User.objects.get(id=user_id)
        except TokenError:
            raise InvalidToken('Token is invalid or expired')
        except User.DoesNotExist:
            raise InvalidToken('User not found')

        new_access_token = new_refresh.access_token
        new_access_token['username'] = user.username
        new_access_token['is_superuser'] = user.is_superuser
        new_access_token['is_staff'] = user.is_staff
        new_access_token['email'] = user.email
        new_access_token['is_active'] = user.is_active
        new_access_token['first_name'] = user.first_name
        new_access_token['is_teacher'] = user.is_teacher
        new_access_token['is_student'] = user.is_student
        new_access_token['last_name'] = user.last_name
        new_access_token['phone_number'] = user.phone_number

        data = {
            'access': str(new_access_token),
            'refresh': str(new_refresh)
        }

        return data




class TeacherSerializer(serializers.ModelSerializer):
    joining_date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    date_of_birth = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Teacher
        exclude = ['groups', 'user_permissions']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Teacher(**validated_data)
        validate_password(password)
        user.set_password(password)
        user.is_staff = True
        user.save()
        return user


class StudentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentImage
        fields = ['id', 'image', 'uploaded_at']

# class StudentCoursesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StudentCourses
#         fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    password = serializers.CharField(write_only=True)
    images = StudentImageSerializer(many=True, read_only=True)
    # courses = StudentCoursesSerializer(many=True, required=False)


    class Meta:
        model = Student
        exclude = ['groups', 'user_permissions']

    def create(self, validated_data):
        # import pdb; pdb.set_trace()
        courses = validated_data.pop('courses', [])
        password = validated_data.pop('password')
        student = Student(**validated_data)
        validate_password(password)
        student.set_password(password)
        student.save()

        return student


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ["id", "name", "username", "password", "channel_number", "ip_address"]


class ClassSerializer(serializers.ModelSerializer):
    cameras = CameraSerializer(many=True, required=False)

    class Meta:
        model = Class
        fields = ["id", "name", "block", "cameras"]

    def create(self, validated_data):
        cameras_data = validated_data.pop("cameras", [])
        class_instance = Class.objects.create(**validated_data)

        for camera_data in cameras_data:
            Camera.objects.create(class_ref=class_instance, **camera_data)

        return class_instance

    def update(self, instance, validated_data):
        cameras_data = validated_data.pop("cameras", [])
        instance.name = validated_data.get("name", instance.name)
        instance.block = validated_data.get("block", instance.block)
        instance.save()

        instance.cameras.all().delete()
        for camera_data in cameras_data:
            Camera.objects.create(class_ref=instance, **camera_data)

        return instance


class SetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data.get('uid')))
            user = User.objects.get(pk=uid)
        except Exception:
            raise serializers.ValidationError({'uid': 'Invalid uid'})

        token = data.get('token')
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise serializers.ValidationError({'token': 'Invalid or expired token'})

        # validate password using Django validators
        validate_password(data.get('password'), user=user)

        data['user'] = user
        return data

#class CourseSerializer(serializers.ModelSerializer):
 #   instructor = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())

  #  class Meta:
   #     model = Course
    #    fields = ['name', 'prereq', 'instructor']

    #def create(self, validated_data):
     #   instructor_data = validated_data.pop('instructor', None)
#
 #       if instructor_data:
  #          instructor_instance, _ = Teacher.objects.get_or_create(**instructor_data)
   #         validated_data['instructor'] = instructor_instance
#
 #       course_instance = Course.objects.create(**validated_data)
  #      return course_instance


# class CourseSerializer(serializers.ModelSerializer):
#     instructor = serializers.CharField()  # now a simple text field

#     class Meta:
#         model = Course
#         fields = ['id','name', 'prereq', 'instructor']

#     def create(self, validated_data):
#         instructor_name = validated_data.pop('instructor')
#         name_parts = instructor_name.strip().split()

#         # Split into first and last name safely
#         first_name = name_parts[0]
#         last_name = name_parts[1] if len(name_parts) > 1 else ""

#         # Try to find matching teacher (case-insensitive)
#         instructor_instance = Teacher.objects.filter(
#             Q(first_name__iexact=first_name) & Q(last_name__iexact=last_name)
#         ).first()

#         if not instructor_instance:
#             raise serializers.ValidationError({
#                 "instructor": f"No teacher found with name '{instructor_name}'."
#             })

#         # Create course with that instructor
#         course_instance = Course.objects.create(
#             instructor=instructor_instance, **validated_data
#         )

#         return course_instance

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.CharField(required=False)
    students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'prereq', 'instructor', 'students']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = str(instance.id)
        if instance.instructor:
            rep['instructor'] = f"{instance.instructor.first_name} {instance.instructor.last_name}".strip()
        # include enrolled students in a compact form, always output id as string
        rep['students'] = [
            {
                'id': str(s.id),
                'first_name': s.first_name,
                'last_name': s.last_name,
                'email': s.email
            }
            for s in instance.students.all()
        ]
        return rep

    def get_students(self, instance):
        return [
            {
                'id': str(s.id),
                'first_name': s.first_name,
                'last_name': s.last_name,
                'email': s.email,
            }
            for s in instance.students.all()
        ]

    def create(self, validated_data):
        instructor_id = validated_data.pop('instructor', '').strip()
        instructor_instance = None
        if instructor_id:
            instructor_instance = Teacher.objects.filter(id=instructor_id).first()

            if not instructor_instance:
                raise serializers.ValidationError({
                    "instructor": f"No teacher found."
                })

        course_instance = Course.objects.create(
            instructor=instructor_instance,
            **validated_data
        )
        return course_instance

    def update(self, instance, validated_data):
        instructor_name = validated_data.pop('instructor', '').strip()
        if instructor_name:
            name_parts = instructor_name.split()
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            instructor_instance = Teacher.objects.filter(
                Q(first_name__iexact=first_name) & Q(last_name__iexact=last_name)
            ).first()

            if not instructor_instance:
                raise serializers.ValidationError({
                    "instructor": f"No teacher found with name '{instructor_name}'."
                })

            instance.instructor = instructor_instance

        # Update remaining fields
        instance.name = validated_data.get('name', instance.name)
        instance.prereq = validated_data.get('prereq', instance.prereq)
        instance.save()
        return instance