import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Lista de datos simulada con IDs string y emails
data_list = [
    {'id': '1', 'name': 'Item 1', 'email': 'uno@email.com', 'is_active': True},
    {'id': '2', 'name': 'Item 2', 'email': 'dos@email.com', 'is_active': False},
    {'id': '3', 'name': 'Item 3', 'email': 'tres@email.com', 'is_active': True},
]

class DemoRestApi(APIView):
    def get(self, request):
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data

        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)
    
class DemoRestApiItem(APIView):

    def find_item(self, item_id):
        return next((item for item in data_list if str(item['id']) == str(item_id)), None)
    
    def get(self, request, item_id):
        item = self.find_item(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(item, status=status.HTTP_200_OK)

    def put(self, request, item_id):
        data = request.data

        if 'id' not in data or str(data['id']) != str(item_id):
            return Response({'error': 'El campo "id" es obligatorio y debe coincidir con el de la URL.'},
                            status=status.HTTP_400_BAD_REQUEST)

        item = self.find_item(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item.clear()
        item.update({
            'id': item_id,
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'is_active': True
        })

        return Response({'message': 'Elemento reemplazado correctamente.', 'data': item},
                        status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        item = self.find_item(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Actualiza solo campos permitidos (opcional)
        for key in ['name', 'email', 'is_active']:
            if key in request.data:
                item[key] = request.data[key]

        return Response({'message': 'Elemento actualizado parcialmente.', 'data': item},
                        status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        item = self.find_item(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item['is_active'] = False
        return Response({'message': 'Elemento eliminado (lógicamente).'}, status=status.HTTP_200_OK)
    