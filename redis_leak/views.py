from django.http import HttpResponse

from redis_leak.celery import debug_task

def run_task(request):
    res = debug_task.apply_async()
    result = res.get()
    return HttpResponse("foo")
