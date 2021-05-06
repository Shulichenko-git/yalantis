from django.urls import path
from courses.views import about, course_add, course_list, course_details, course_filter, course_edit, course_delete

urlpatterns = [
    path('', about),
    path('course-add/', course_add),
    path('course-list/', course_list),
    path('course-details/', course_details),
    path('course-filter/', course_filter),
    path('course-edit/', course_edit),
    path('course-delete/', course_delete),
]