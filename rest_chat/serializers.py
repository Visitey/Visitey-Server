from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

from rest_chat.models import Message, NotificationCheck, Thread, Participant
from rest_profile.models import Profile


class ParticipantSerializer(FriendlyErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail', queryset=Profile.objects.all())

    class Meta:
        model = Participant
        fields = '__all__'


class ThreadSerializer(FriendlyErrorMessagesMixin, serializers.HyperlinkedModelSerializer):
    participants = serializers.HyperlinkedRelatedField(many=True, view_name='profile-detail',
                                                       queryset=Profile.objects.all())
    removable_participants_ids = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Don't pass the 'callback' arg up to the superclass
        self.callback = kwargs.pop('callback', None)
        # Instantiate the superclass normally
        super(ThreadSerializer, self).__init__(*args, **kwargs)

    def get_participants(self, obj):
        """ Allows to define a callback for serializing information about the user. """
        # we set the many to many serialization to False, because we only want it with retrieve requests
        if self.callback is None:
            return [participant.id for participant in obj.participants.all()]
        else:
            # we do not want user information
            return self.callback(obj)

    def get_removable_participants_ids(self, obj):
        """ Get the participants that can be removed from the thread. """
        return obj.get_removable_participants_ids(self.context.get('request', None))


class SimpleMessageSerializer(serializers.ModelSerializer):
    """ Returns the messages without complementary information. """

    class Meta:
        model = Message
        fields = ('id', 'body', 'sender', 'thread', 'sent_at')


class ComplexMessageSerializer(serializers.ModelSerializer):
    is_notification = serializers.SerializerMethodField()
    readers = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id', 'body', 'sender', 'thread', 'sent_at', 'is_notification', 'readers')

    def get_is_notification(self, obj):
        """ We say if the message should trigger a notification """
        try:
            o = obj
            return o.is_notification
        except Exception:
            return False

    def get_readers(self, obj):
        """ Return the ids of the people who read the message instance. """
        try:
            o = obj
            return o.readers
        except Exception:
            return []


class MessageNotificationCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationCheck
        fields = '__all__'
