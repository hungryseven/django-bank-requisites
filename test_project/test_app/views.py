from rest_framework import viewsets

from .models import OrganizationValidated, OrganizationUnvalidated
from .serializers import ValidatedModelSerializer, UnvalidatedModelSerializer

class ValidatedModelViewSet(viewsets.ModelViewSet):

    queryset = OrganizationValidated.objects.all()
    serializer_class = ValidatedModelSerializer

class UnvalidatedModelViewSet(viewsets.ModelViewSet):

    queryset = OrganizationUnvalidated.objects.all()
    serializer_class = UnvalidatedModelSerializer
