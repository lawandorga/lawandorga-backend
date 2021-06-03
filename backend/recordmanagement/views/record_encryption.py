from backend.recordmanagement.models.record_encryption import RecordEncryption
from backend.recordmanagement.serializers import RecordEncryptionSerializer
from rest_framework.viewsets import ModelViewSet


class RecordEncryptionViewSet(ModelViewSet):
    queryset = RecordEncryption.objects.all()
    serializer_class = RecordEncryptionSerializer
