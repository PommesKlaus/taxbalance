from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from core.models import Version
from localgaap.models import Transaction
from localgaap.serializers import TransactionSerializer


class TransactionCreateView(CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        version = Version.objects.get(pk=self.request.data.get("version"))
        if version.locked or version.archived:
            raise ValidationError('Version is locked or archived.')
            #TODO: Create test for locked or archived version
        # Save Version to create new updated_at timestamp
        version.save()
        serializer.save()


class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        version = Version.objects.get(pk=self.request.data.get("version"))
        if version.locked or version.archived:
            raise ValidationError('Version is locked or archived.')
            #TODO: Create test for locked or archived version
        # Save Version to create new updated_at timestamp
        version.save()
        serializer.save()
