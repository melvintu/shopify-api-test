import logging
from fastapi.responses import Response

# This is for logging 

logger = logging.getLogger(__name__)

def shopify_result_to_response(result):
    logger.info("%s - %s", result.log.code, result.log.detail)

    return Response(
        content=result.response.body,
        status_code=result.response.status,
        headers=result.response.headers,
    )