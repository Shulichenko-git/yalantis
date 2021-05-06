from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from courses.models import Course


def about(request):
    data = {
        'about': 'Hello! You may to check it with POSTMAN!'
    }
    return JsonResponse(data)


@csrf_exempt
def course_add(request):
    if request.method != 'POST':
        return JsonResponse({'status': 402,
                             'msg': 'Wrong method'})

    title = request.POST.get('title')
    date_of_start = request.POST.get('date_of_start')
    date_of_finish = request.POST.get('date_of_finish')
    number_of_lectures = request.POST.get('number_of_lectures')

    if date_of_finish < date_of_start:
        return JsonResponse({'Warning': 'Finish must be later than Start!'})
    try:
        number_of_lectures = int(number_of_lectures)
    except ValueError:
        return JsonResponse({'status': 403,
                             'msg': 'Number must be a digit'})
    if number_of_lectures <= 0:
        return JsonResponse({'status': 403,
                             'msg': 'Number must be a positive'})
    if not title or not date_of_start or not date_of_finish or not number_of_lectures:
        return JsonResponse({'status': 403,
                             'msg': 'Wrong data'})

    course = Course(
        title=title,
        date_of_start=date_of_start,
        date_of_finish=date_of_finish,
        number_of_lectures=number_of_lectures
    )
    try:
        course.save()
    except ValidationError:
        return JsonResponse({'status': 403,
                             'msg': 'Wrong data'})

    return JsonResponse({'status': 200, 'msg': 'OK'})


def course_list(request):
    courses = Course.objects.all()

    normalized_courses = []
    for course in courses:
        normalized_course = {
            'title': course.title,
            'date_of_start': course.date_of_start,
            'date_of_finish': course.date_of_finish,
            'number_of_lectures': course.number_of_lectures
        }
        normalized_courses.append(normalized_course)

    return JsonResponse({'courses': normalized_courses})


def course_details(request):
    pk = request.GET.get('pk')
    try:
        pk = int(pk)
    except ValueError:
        return JsonResponse({'status': 403,
                             'msg': 'Wrong data'})

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({'status': 404,
                             'msg': 'Missing data'})

    normalized_course = {
        'title': course.title,
        'date_of_start': course.date_of_start,
        'date_of_finish': course.date_of_finish,
        'number_of_lectures': course.number_of_lectures
    }
    return JsonResponse({'course': normalized_course})


def course_filter(request):
    title = request.GET.get('title')
    date_of_start = request.GET.get('date_of_start')
    date_of_finish = request.GET.get('date_of_finish')

    courses = Course.objects.all()

    if title:
        courses = courses.filter(title=title)

    if date_of_start:
        courses = courses.filter(date_of_start=date_of_start)

    if date_of_finish:
        courses = courses.filter(date_of_finish=date_of_finish)

    normalized_courses = []
    for course in courses:
        normalized_course = {
            'title': course.title,
            'date_of_start': course.date_of_start,
            'date_of_finish': course.date_of_finish,
            'number_of_lectures': course.number_of_lectures
        }
        normalized_courses.append(normalized_course)

    return JsonResponse({'courses': normalized_courses})


@csrf_exempt
def course_edit(request):
    if request.method != 'POST':
        return JsonResponse({'status': 402, 'msg': 'Wrong method'})
    pk = request.POST.get('pk')
    try:
        pk = int(pk)
    except ValueError:
        return JsonResponse({'status': 403,
                             'msg': 'Wrong data'})
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({'status': 404,
                             'msg': 'Missing DB data'})

    if request.POST.get('title') is None:
        course.title = Course.objects.get(pk=pk).title
    else:
        course.title = request.POST.get('title')

    if request.POST.get('date_of_start') is None:
        course.date_of_start = Course.objects.get(pk=pk).date_of_start
    else:
        course.date_of_start = request.POST.get('date_of_start')

    if request.POST.get('date_of_finish') is None:
        course.date_of_finish = Course.objects.get(pk=pk).date_of_finish
    else:
        course.date_of_finish = request.POST.get('date_of_finish')

    if request.POST.get('number_of_lectures') is None:
        course.number_of_lectures = Course.objects.get(pk=pk).number_of_lectures
    else:
        course.number_of_lectures = request.POST.get('number_of_lectures')

    title = course.title
    date_of_start = course.date_of_start
    date_of_finish = course.date_of_finish
    number_of_lectures = course.number_of_lectures

    if date_of_finish < date_of_start:
        return JsonResponse({'Warning': 'Finish must be later than Start!'})
    try:
        number_of_lectures = int(number_of_lectures)
    except ValueError:
        return JsonResponse({'status': 403,
                             'msg': 'Number must be a digit'})
    if number_of_lectures <= 0:
        return JsonResponse({'status': 403,
                             'msg': 'Number must be a positive'})
    if not title or not date_of_start or not date_of_finish or not number_of_lectures:
        return JsonResponse({'status': 403,
                             'msg': 'Wrong data'})
    try:
        course.save()
    except ValidationError:
        return JsonResponse({'status': 403,
                             'msg': 'Wrong data'})

    return JsonResponse({'status': 200, 'msg': 'OK'})


@csrf_exempt
def course_delete(request):
    if request.method != 'POST':
        return JsonResponse({'status': 402, 'msg': 'Wrong method'})

    pk = request.POST.get('pk')
    try:
        pk = int(pk)
    except ValueError:
        return JsonResponse({'status': 403,
                             'msg': 'Wrong data'})

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({'status': 404,
                             'msg': 'Missing DB data'})

    normalized_course = {
        'title': course.title,
        'date_of_start': course.date_of_start,
        'date_of_finish': course.date_of_finish,
        'number_of_lectures': course.number_of_lectures,
        'status': 'deleted'
    }
    course.delete()
    return JsonResponse({'course': normalized_course})
