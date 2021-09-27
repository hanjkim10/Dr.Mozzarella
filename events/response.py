from drf_yasg import openapi

events_schema_dict = {
    "201": openapi.Response(
        description="데이터 적재 성공",
        examples={
            "application/json": {
                'message': 'SUCCESS',
                "count": 103}})}