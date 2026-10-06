from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count

from cvat.apps.engine.models import Task, LabeledShape, LabeledTrack, LabeledImage
from cvat.apps.engine.views import TaskViewSet

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def annotation_counts(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    # Re-use CVAT's PolicyEnforcer via TaskViewSet
    view = TaskViewSet()
    view.request = request
    view.action = 'retrieve'
    view.format_kwarg = None
    view.kwargs = {'pk': task_id}
    view.check_object_permissions(request, task)

    # Count shapes
    shapes_counts = LabeledShape.objects.filter(
        job__segment__task=task
    ).values('label__name', 'type').annotate(count=Count('id'))

    # Count tracks
    tracks_counts = LabeledTrack.objects.filter(
        job__segment__task=task
    ).values('label__name').annotate(count=Count('id'))

    # Count tags/images
    images_counts = LabeledImage.objects.filter(
        job__segment__task=task
    ).values('label__name').annotate(count=Count('id'))

    counts = {}

    for s in shapes_counts:
        label = s['label__name']
        shape_type = s['type']
        counts.setdefault(label, {'total': 0, 'by_type': {}})
        counts[label]['total'] += s['count']
        counts[label]['by_type'][shape_type] = counts[label]['by_type'].get(shape_type, 0) + s['count']
        
    for t in tracks_counts:
        label = t['label__name']
        shape_type = 'track'
        counts.setdefault(label, {'total': 0, 'by_type': {}})
        counts[label]['total'] += t['count']
        counts[label]['by_type'][shape_type] = counts[label]['by_type'].get(shape_type, 0) + t['count']
        
    for i in images_counts:
        label = i['label__name']
        shape_type = 'tag'
        counts.setdefault(label, {'total': 0, 'by_type': {}})
        counts[label]['total'] += i['count']
        counts[label]['by_type'][shape_type] = counts[label]['by_type'].get(shape_type, 0) + i['count']

    return Response(counts)
