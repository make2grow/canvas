from canvasapi.canvas import Canvas
from . import logger
from . import getinfo

logname = getinfo.get_logname(__file__)
logger = logger.setup_logger(name=__name__, logfile=logname)

def print_python_object(obj):
    """Pretty-print common Python / canvasapi objects safely."""
    def print_canvas_object(obj):
        req = getattr(obj, "_Canvas__requester", None)
        if req is None:
            print("(Canvas has no requester)")
            return
    
        base_url = getattr(req, "base_url", getattr(req, "_Requester__base_url", None))
        per_page = getattr(req, "per_page", getattr(req, "_Requester__per_page", None))
        token = getattr(req, "access_token", getattr(req, "_Requester__access_token", None))
    
        logger.info(f"base_url: {base_url!r}")
        logger.info(f"per_page: {per_page!r}")  # may be None if not exposed in this version
        if token:
            logger.info(f"access_token: {str(token)[:10]}… (masked)")
        return    
    
    print(f"[type] {type(obj)}")

    if isinstance(obj, dict):
        for k, v in obj.items():
            logger.info({k: v})
        return

    if isinstance(obj, list):
        for item in obj:
            print_python_object(item)
        return

    if isinstance(obj, Canvas):
        req = getattr(obj, "_Canvas__requester", None)
        if req is None:
            logger.info("(Canvas has no requester)")
            return

        base_url = getattr(req, "base_url", getattr(req, "_Requester__base_url", None))
        per_page = getattr(req, "per_page", getattr(req, "_Requester__per_page", None))
        token = getattr(req, "access_token", getattr(req, "_Requester__access_token", None))

        logger.info(f"base_url: {base_url!r}")
        logger.info(f"per_page: {per_page!r}")  # may be None if not exposed in this version
        if token:
            logger.info(f"access_token: {str(token)[:6]}… (masked)")
        return

    # Generic: show instance attributes if present
    if hasattr(obj, "__dict__"):
        logger.info(vars(obj))
    else:
        logger.info(obj)