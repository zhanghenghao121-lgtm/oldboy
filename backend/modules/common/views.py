from django.utils.timezone import now
from rest_framework.decorators import api_view
from modules.common.response import ok


@api_view(["GET"])
def healthz(request):
    return ok({"status": "ok", "timestamp": now().isoformat()})
