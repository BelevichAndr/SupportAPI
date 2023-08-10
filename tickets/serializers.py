from rest_framework import serializers

from tickets.models import ClientMessage, SupportSystemMessage, Ticket


class TicketSerializer(serializers.ModelSerializer):

    creator = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = Ticket
        fields = ("pk", "creator", "subject", "message", "status", "created_at", "updated_at")


class TicketCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("pk", "subject", "message", "created_at", "updated_at")


class TicketSupportUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("status", )


class SupportSystemTicketMessageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    ticket = serializers.SlugRelatedField(slug_field="subject", read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = SupportSystemMessage
        fields = ["pk", "user", "ticket", "message", "parent_message", "created_at", "replies"]

    def get_replies(self, obj):
        if obj.support_replies.exists():
            serializer = ClientTicketMessageSerializer(obj.support_replies.all(), many=True)
            return serializer.data
        return []


class ClientTicketMessageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    ticket = serializers.SlugRelatedField(slug_field="subject", read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = ClientMessage
        fields = ["pk", "user", "ticket", "message", "parent_message", "created_at", "replies"]

    def get_replies(self, obj):
        if obj.client_replies.exists():
            serializer = SupportSystemTicketMessageSerializer(obj.client_replies.all(), many=True)
            return serializer.data
        return []


class ClientMessageCreateSerializer(serializers.ModelSerializer):
    """ For creation messages"""
    ticket = serializers.SlugRelatedField(slug_field="subject", read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = ClientMessage
        fields = ["pk", "user", "ticket", "message", "parent_message", "created_at"]


class SupportMessageCreateSerializer(serializers.ModelSerializer):
    """ For creation messages"""
    ticket = serializers.SlugRelatedField(slug_field="subject", read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SupportSystemMessage
        fields = ["pk", "user", "ticket", "message", "parent_message", "created_at"]