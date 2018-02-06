from rest_framework import permissions, viewsets

from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
	lookup_field = 'username'
	queryset = Account.objects.all()
	serializers_class = AccountSerializer

	def get_permissions(self):
		if self.request.method in permissions.SAFE_METHODS:
			return (permissions.AllowAny(),)

		if self.request.method == 'POST':
			return (permission.AllowAny(),)

		return (permissions.IsAuthenticated(), IsAccountOwner(),)

	def create(self, request):
		serializer = self.serializers_class(data=request.data)

		if serializer.is_valid():
			Account.objects.create_user(**serializer.validated_data)

			return Response(serializer.validated_data, status=Status.HTTP_201_CREATED)

		return Response({
			'status': 'Bad request',
			'message': 'Account could not be created with received data.'
			}, status = status.HTTP_400_BAD_REQUEST)