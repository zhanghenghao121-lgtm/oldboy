from rest_framework.response import Response


def ok(data=None, message="ok", code=0):
    return Response({"code": code, "message": message, "data": data or {}})


def fail(message="error", code=1, data=None, status=400):
    return Response({"code": code, "message": message, "data": data or {}}, status=status)
