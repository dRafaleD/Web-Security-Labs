"""Offline error response mapper. No HTTP server."""
def response(error, request_id):
    mapping = {"bad_input": (400, "INVALID_REQUEST"),
               "unauthorized": (401, "AUTH_REQUIRED")}
    status, code = mapping.get(error, (500, "INTERNAL_ERROR"))
    return {"status": status, "body": {"code": code, "request_id": request_id}}

for err in ["bad_input", "unauthorized", "database-secret-password"]:
    result = response(err, "demo-001")
    print(result)
    assert "password" not in str(result)
    assert "Traceback" not in str(result)
assert response("unknown", "demo-001")["status"] == 500
