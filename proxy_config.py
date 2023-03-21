import os

REMOTE_HOST = "localhost"
REMOTE_CDN = "localhost"
REMOTE_GATEWAY = "localhost"
REMOTE_PORT = 3000
CDN_PORT = 3001
WS_PORT = 3002
VOICE_PORT = 3015
USE_HTTPS = False

SCHEME = "http"
if USE_HTTPS:
    SCHEME = "https"

if os.getenv("REMOTE_HOST") != None:
    REMOTE_HOST = os.getenv("REMOTE_HOST")
if os.getenv("REMOTE_CDN") != None:
    REMOTE_CDN = os.getenv("REMOTE_CDN")
if os.getenv("REMOTE_GATEWAY") != None:
    REMOTE_GATEWAY = os.getenv("REMOTE_GATEWAY")

if os.getenv("REMOTE_PORT") != None:
    REMOTE_PORT = os.getenv("REMOTE_PORT")
if (os.getenv("CDN_PORT")) != None:
    CDN_PORT = os.getenv("CDN_PORT")
if os.getenv("WS_PORT") != None:
    WS_PORT = os.getenv("WS_PORT")

if os.getenv("USE_HTTPS") != None:
    USE_HTTPS = bool(os.getenv("USE_HTTPS"))

print("Server address:", REMOTE_HOST)
print("CDN Address:", REMOTE_CDN)
print("Gateway Address:", REMOTE_GATEWAY)

print("Server port:", REMOTE_PORT)
print("Scheme:", SCHEME)