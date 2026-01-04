from django.urls import path
from .views import (MyTokenObtainPairView, MyTokenRefreshView, course_api, course_by_id_api, index, teacher_api,
                    teacher_by_id_api, reset_password_confirm_link, student_api, student_by_id_api, class_api,
                    class_by_id_api, upload_student_image, course_students_api, course_mark_attendance_api, start_attendance_api, stop_attendance_api,
                    lecture_api, get_attendance_details_by_lecture)
from .views import set_password_api

app_name = 'users'

urlpatterns = [
    path('', index, name='home'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('teacher/', teacher_api, name='teacher api'),
    path('student/', student_api, name='student api'),
    path('class/', class_api, name='class api'),
    path('teacher/<str:teacher_id>/', teacher_by_id_api, name='teacher by id api'),
    path('student/<str:student_id>/', student_by_id_api, name='student by id api'),
    path('class/<str:class_id>/', class_by_id_api, name='class by id api'),
    path('reset-password-confirm/', reset_password_confirm_link, name='reset_password_confirm_link'),
    path('set-password/', set_password_api, name='set_password'),
    path('student/<str:student_id>/upload-images/', upload_student_image, name='upload_student_image'),
    path('course/', course_api, name='course api'),
    path('course/<str:course_id>/students/', course_students_api, name='course students api'),
    path('course/<str:course_id>/', course_by_id_api, name='course by id api'),
    path('course/<str:course_id>/attendance/', course_mark_attendance_api, name='course mark attendance'),
    path('start-attendance/', start_attendance_api, name='start_attendance_api'),
    path('stop-attendance/<str:lecture_id>/', stop_attendance_api, name='stop_attendance_api'),
    path('lecture/', lecture_api, name='lecture_api'),
    path('attendance/<str:lecture_id>/', get_attendance_details_by_lecture, name='get_attendance_details_by_lecture'),
]
