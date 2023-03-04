from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Fighter
from django.core import serializers
from django.http import HttpResponse
import json


def index(request):
    fighter_list = Fighter.objects.order_by('-name')[:5]
    output = ', '.join([q.name for q in fighter_list])
    return HttpResponse(output)

def detail(request, fighter_id):
    fighter = get_object_or_404(Fighter, pk=fighter_id)
    events = fighter.event_set.all()
    serialized_event = serializers.serialize('json',events)
    print(serialized_event)
    serialized_fighter = serializers.serialize('json',[fighter, ])
    return HttpResponse(serialized_fighter, content_type="application/json")
    #return JsonResponse(serialized_fighter)

def fighter_events(request, fighter_id):
    fighter = get_object_or_404(Fighter, pk=fighter_id)
    events = fighter.event_set.all()
    serialized_event = serializers.serialize('json',events)
    return HttpResponse(serialized_event, content_type="application/json")
    #return JsonResponse(serialized_fighter)