from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    current_visitors = Visit.objects.filter(leaved_at=None)
    serialized_non_closed_visits = []
    for current_visitor in current_visitors:
        who_entered = current_visitor.passcard.owner_name
        entered_at = current_visitor.entered_at
        duration = current_visitor.format_duration()
        is_strange = current_visitor.is_visit_long()
        serialized_non_closed_visits.append({'who_entered': who_entered,
                                  'entered_at': entered_at,
                                  'duration': duration,
                                  'is_strange': is_strange})

    context = {
        'non_closed_visits': serialized_non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
