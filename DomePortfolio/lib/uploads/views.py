from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError
import json


def upload_progress(request):
    """
    A view to report back on upload progress.

    :return: JSON object with information about the progress of an upload.
    """
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        cache_key = f"{request.META.get('REMOTE_ADDR')}_{progress_id}"
        data = cache.get(cache_key)
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponseServerError(
            'Server Error: You must provide X-Progress-ID header or query param.'
        )
