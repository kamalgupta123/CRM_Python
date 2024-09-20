from rest_framework import serializers
from .models import *

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        depth = 1

class ChatterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatter
        fields = "__all__"

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"

class LeadItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadItem
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class LeadAttachmentSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = LeadAttachment
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
