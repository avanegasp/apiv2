import logging

from capyc.rest_framework.exceptions import ValidationException
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from breathecode.utils import APIViewExtensions, GenerateLookupsMixin

from .actions import get_template_content
from .models import Hook, Notification, SlackTeam
from .serializers import HookSerializer, NotificationSerializer, SlackTeamSerializer
from .tasks import async_slack_action, async_slack_command

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([AllowAny])
def preview_template(request, slug):
    template = get_template_content(slug, request.GET, formats=["html"])
    return HttpResponse(template["html"])


@api_view(["GET"])
@permission_classes([AllowAny])
def preview_slack_template(request, slug):
    template = get_template_content(slug, request.GET, ["slack"])
    return HttpResponse(template["slack"])


@api_view(["GET"])
@permission_classes([AllowAny])
def test_email(request, email):
    # tags = sync_user_issues()
    # return Response(tags, status=status.HTTP_200_OK)
    pass


@api_view(["POST"])
@permission_classes([AllowAny])
def process_interaction(request):
    try:
        async_slack_action.delay(request.POST)
        logger.debug("Slack action enqueued")
        return Response("Processing...", status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("Error processing slack action")
        return Response(str(e), status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def slack_command(request):

    try:
        async_slack_command.delay(request.data)
        logger.debug("Slack command enqueued")
        return Response("Processing...", status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("Error processing slack command")
        return Response(str(e), status=status.HTTP_200_OK)


@api_view(["GET"])
def get_sample_data(request, hook_id=None):

    if hook_id is not None:
        hook = Hook.objects.filter(user__id=request.user.id, id=hook_id).first()
        if hook is None:
            return Response(
                {"details": "No hook found with this filters for sample data"}, status=status.HTTP_400_BAD_REQUEST
            )

        if hook.sample_data is None:
            return Response([])

        return Response(hook.sample_data)

    items = Hook.objects.filter(user__id=request.user.id)
    filtered = False
    event = request.GET.get("event", None)
    if event is not None:
        filtered = True
        items = items.filter(event__in=event.split(","))

    service_id = request.GET.get("service_id", None)
    if service_id is not None:
        filtered = True
        items = items.filter(service_id__in=service_id.split(","))

    like = request.GET.get("like", None)

    if like is not None:
        items = items.filter(Q(event__icontains=like) | Q(target__icontains=like))

    if not filtered:
        return Response(
            {"details": "Please specify hook id or filters get have an idea on what sample data you want"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    single = items.first()
    if single is None:
        return Response(
            {"details": "No hook found with this filters for sample data"}, status=status.HTTP_400_BAD_REQUEST
        )

    return Response(single.sample_data)


class HooksView(APIView, GenerateLookupsMixin):
    """
    List all snippets, or create a new snippet.
    """

    extensions = APIViewExtensions(sort="-created_at", paginate=True)

    def get(self, request):
        handler = self.extensions(request)

        items = Hook.objects.filter(user__id=request.user.id)

        event = request.GET.get("event", None)
        if event is not None:
            items = items.filter(event__in=event.split(","))

        service_id = request.GET.get("service_id", None)
        if service_id is not None:
            items = items.filter(service_id__in=service_id.split(","))

        like = request.GET.get("like", None)
        if like is not None:
            items = items.filter(Q(event__icontains=like) | Q(target__icontains=like))

        items = handler.queryset(items)
        serializer = HookSerializer(items, many=True)

        return handler.response(serializer.data)

    def post(self, request):

        serializer = HookSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, hook_id):

        hook = Hook.objects.filter(id=hook_id, user__id=request.user.id).first()
        if hook is None:
            raise ValidationException(f"Hook {hook_id} not found for this user", slug="hook-not-found")

        serializer = HookSerializer(
            instance=hook,
            data=request.data,
            context={
                "request": request,
            },
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, hook_id=None):

        filtered = False
        items = Hook.objects.filter(user__id=request.user.id)
        if hook_id is not None:
            items = items.filter(id=hook_id)
            filtered = True
        else:
            event = request.GET.get("event", None)
            if event is not None:
                filtered = True
                items = items.filter(event__in=event.split(","))

            service_id = request.GET.get("service_id", None)
            if service_id is not None:
                filtered = True
                items = items.filter(service_id__in=service_id.split(","))

        if not filtered:
            raise ValidationException("Please include some filter in the URL")

        total = items.count()
        for item in items:
            item.delete()

        return Response({"details": f"Unsubscribed from {total} hooks"}, status=status.HTTP_200_OK)


class SlackTeamsView(APIView, GenerateLookupsMixin):
    """
    List all snippets, or create a new snippet.
    """

    extensions = APIViewExtensions(sort="-created_at", paginate=True)

    def get(self, request):
        handler = self.extensions(request)

        items = SlackTeam.objects.all()
        academy = request.GET.get("academy", None)
        if academy is not None:
            academy = academy.split(",")
            items = items.filter(academy__slug__in=academy)

        items = handler.queryset(items)
        serializer = SlackTeamSerializer(items, many=True)

        return handler.response(serializer.data)


class NotificationsView(APIView, GenerateLookupsMixin):
    extensions = APIViewExtensions(sort="-id", paginate=True)

    def get(self, request):
        handler = self.extensions(request)
        items = Notification.objects.filter(user__id=request.user.id)

        if (academies := request.GET.get("academy")) is not None:
            academies = academies.split(",")
            items = items.filter(academy__slug__in=academies)

        if (done_at := request.GET.get("done_at")) is not None:
            items = items.filter(done_at__gte=done_at)

        if request.GET.get("seen") == "true":
            items = items.filter(seen_at__isnull=False)

        items = handler.queryset(items)

        ids = [x.id for x in items if x.seen_at is None]
        if ids:
            Notification.objects.filter(id__in=ids).update(seen_at=timezone.now())

        serializer = NotificationSerializer(items, many=True)
        return handler.response(serializer.data)
