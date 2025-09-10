import os

def getKey(DEBUG_MODE=False):
    CCTV_API_KEY = os.environ.get('CCTV_API_KEY', None)
    if CCTV_API_KEY is None:
        if DEBUG_MODE: print("[ERROR] ValueError: CCTV_API_KEY environment variable not set")
        return None

    return CCTV_API_KEY