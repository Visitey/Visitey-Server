from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

from rest_chat.models import Participant


class MessagingMiddleware(MiddlewareMixin):
    """
    Ensures we can access request.user as request.rest_messaging_participant in every request.
    """

    def process_view(self, request, callback, callback_args, callback_kwargs):

        assert hasattr(request, 'user'), (
            "The django-rest-messaging MessagingMiddleware requires an authentication middleware "
            "to be installed because request.user must be available."
        )

        if request.user.is_authenticated:

            participant = cache.get('rest_messaging_participant_{0}'.format(request.user.id), None)

            if participant is None:
                # either we create the participant or we retrieve him
                try:
                    participant = Participant.objects.get(id=request.user.id)
                except:
                    participant = Participant.objects.create(id=request.user.id)
                # cached for 60 minutes
                cache.set('rest_messaging_participant_{0}'.format(request.user.id), participant, 60 * 60)
        else:
            participant = None

        request.rest_messaging_participant = participant

        return None
