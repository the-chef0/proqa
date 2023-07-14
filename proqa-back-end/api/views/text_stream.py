from django.http import HttpResponse, HttpResponseNotAllowed
from django_grip import set_hold_stream


def text_stream(request):
    """
    Opens a text stream for the user.
        Args:
            request (HttpRequest): The request object.
        Returns:
            HttpResponse: A HTTP response containing the text stream.
    """
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    if not request.grip_proxied:
        return HttpResponse('Not Implemented\n', status=501)
    resp = HttpResponse('[stream open]\n', content_type='text/event-stream')
    channel = request.user.username
    if not channel:
        return HttpResponse('Channel not provided\n', status=400)
    set_hold_stream(request, channel)
    return resp
