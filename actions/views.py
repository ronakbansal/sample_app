from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import HttpResponse, JsonResponse
import slack

@csrf_exempt
def event_hook(request):
    client = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)
    json_dict = json.loads(request.body.decode('utf-8'))

    if json_dict['token'] != settings.VERIFICATION_TOKEN:
        return HttpResponse(status=403)

    if 'type' in json_dict:
        if json_dict['type'] == 'url_verification':
            response_dict = {"challenge": json_dict['challenge']}
            return JsonResponse(response_dict, safe=False)

    if 'event' in json_dict:
        print(json_dict)
        event_msg = json_dict['event']
        if ('subtype' in event_msg) and (event_msg['subtype'] == 'bot_message'):
            return HttpResponse(status=200)

        if event_msg['type'] == 'message':
            user = event_msg['user']
            channel = event_msg['channel']
            response_msg = ":wave:, Hello <@%s>" % user
            client.chat_postMessage(channel=channel, text=response_msg)
            return HttpResponse(status=200)
    return HttpResponse(status=200)
