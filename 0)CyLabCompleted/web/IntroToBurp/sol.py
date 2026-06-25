from base64 import b64decode
import zlib

URL = ""

def decode(cookie):
    """Decode a Flask cookie."""
    try:
        compressed = False
        payload = cookie

        if payload.startswith('.'):
            compressed = True
            payload = payload[1:]

        data = payload.split(".")[0]

        data = b64decode(data)
        if compressed:
            data = zlib.decompress(data)

        return data.decode("utf-8")
    except Exception as e:
        return "[Decoding error: are you sure this was a Flask session cookie? {}]".format(e)
    