from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

# “Base de datos” en memoria
data_list = [
    {'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True},
    {'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True},
    {'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False},
]

class DemoRestApi(APIView):
    """
    GET  -> lista de elementos activos
    POST -> crear nuevo elemento
    """
    def get(self, request):
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response(
                {'error': "Faltan 'name' o 'email'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)
        return Response(
            {'message': 'Creado.', 'data': data},
            status=status.HTTP_201_CREATED
        )


class DemoRestApiItem(APIView):
    """
    GET    -> detalle de un elemento
    PUT    -> reemplazo completo
    PATCH  -> actualización parcial
    DELETE -> eliminación lógica
    """
    def get(self, request, item_id):
        for item in data_list:
            if item['id'] == item_id:
                return Response(item, status=status.HTTP_200_OK)
        return Response({'error': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, item_id):
        for idx, item in enumerate(data_list):
            if item['id'] == item_id:
                new_data = request.data
                if new_data.get('id') != item_id:
                    return Response(
                        {'error': "El 'id' debe coincidir con la URL."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                new_data['is_active'] = new_data.get('is_active', item['is_active'])
                data_list[idx] = new_data
                return Response({'message': 'Reemplazado.', 'data': new_data})
        return Response({'error': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, item_id):
        for item in data_list:
            if item['id'] == item_id:
                for k, v in request.data.items():
                    if k in item and k != 'id':
                        item[k] = v
                return Response({'message': 'Actualizado.', 'data': item})
        return Response({'error': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, item_id):
        for item in data_list:
            if item['id'] == item_id:
                item['is_active'] = False
                return Response({'message': 'Desactivado.', 'data': item})
        return Response({'error': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
