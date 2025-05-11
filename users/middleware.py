from django.utils import timezone
from .models import AuditLog
import json

class HIPAAComplianceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Procesar la solicitud
        response = self.get_response(request)

        # Registrar la actividad
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                # Obtener detalles de la solicitud
                path = request.path
                method = request.method
                ip = self.get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', '')

                # Determinar el tipo de recurso y acción
                resource_type = self.get_resource_type(path)
                action = self.get_action_type(method)

                # Crear registro de auditoría
                AuditLog.objects.create(
                    user=request.user,
                    action=action,
                    resource_type=resource_type,
                    resource_id=self.get_resource_id(path),
                    ip_address=ip,
                    user_agent=user_agent,
                    success=200 <= response.status_code < 400,
                    details=self.get_request_details(request)
                )
            except Exception as e:
                # Registrar error en los logs del sistema
                print(f"Error en HIPAAComplianceMiddleware: {str(e)}")

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def get_resource_type(self, path):
        # Mapear la ruta a un tipo de recurso
        if '/graphql' in path:
            return 'GraphQL'
        # Agregar más mapeos según sea necesario
        return 'Unknown'

    def get_action_type(self, method):
        # Mapear método HTTP a tipo de acción
        method_map = {
            'GET': 'READ',
            'POST': 'CREATE',
            'PUT': 'UPDATE',
            'PATCH': 'UPDATE',
            'DELETE': 'DELETE'
        }
        return method_map.get(method, 'UNKNOWN')

    def get_resource_id(self, path):
        # Extraer ID del recurso de la ruta si está presente
        # Implementar según la estructura de URLs
        return 'N/A'

    def get_request_details(self, request):
        details = {
            'path': request.path,
            'method': request.method,
            'timestamp': timezone.now().isoformat()
        }
        
        # Agregar datos del body si es POST/PUT/PATCH
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                # Sanitizar datos sensibles antes de guardar
                body = request.body.decode('utf-8')
                # Implementar lógica de sanitización aquí
                details['body'] = 'REDACTED'  # No guardar datos sensibles
            except:
                details['body'] = 'ERROR_PARSING_BODY'

        return json.dumps(details)