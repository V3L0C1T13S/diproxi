"""
A simple script that proxies a certain chat app client.

Notes:

    This script requires a mitmproxy to be run with these options:
        --ssl-insecure --set upstream_cert=false

Usage:

    mitmproxy --ssl-insecure --set upstream_cert=false -s dsc_proxy.py
"""
import logging

from mitmproxy import ctx, http
from proxy_config import REMOTE_HOST, REMOTE_CDN, REMOTE_GATEWAY, REMOTE_PORT, CDN_PORT, WS_PORT, BLOCK_ESSENTIAL_DOMAINS, SCHEME

APP_BRANCH_DOMAINS = ["discord.com", "canary.discord.com", "ptb.discord.com"]
CDN_DOMAINS = ["cdn.discordapp.com"]
APP_DOMAINS = APP_BRANCH_DOMAINS + CDN_DOMAINS + ["discordapp.com", "gateway.discord.gg"]

ESSENTIAL_API_PATHS = ["modules"]
ESSENTIAL_CDN_PATHS = ["changelogs"]

class ChatAppProxy:
    def load(self, loader):
        logging.info("loaded!")

    def request(self, flow: http.HTTPFlow) -> None:
        if flow.request.host in APP_DOMAINS:
            if flow.request.host in APP_BRANCH_DOMAINS:
                if flow.request.path.startswith("/api"):
                    if flow.request.path_components[1] in ESSENTIAL_API_PATHS and not BLOCK_ESSENTIAL_DOMAINS:
                        return
                    flow.request.scheme = SCHEME
                    flow.request.host = REMOTE_HOST
                    flow.request.port = REMOTE_PORT
            elif flow.request.pretty_url.startswith("https://cdn.discordapp.com"):
                if not BLOCK_ESSENTIAL_DOMAINS and flow.request.path_components[0] in ESSENTIAL_CDN_PATHS:
                    return
                flow.request.scheme = SCHEME
                flow.request.host = REMOTE_CDN
                flow.request.port = CDN_PORT
            elif flow.request.pretty_url.startswith("https://gateway.discord.gg"):
                flow.request.scheme = SCHEME
                flow.request.host = REMOTE_GATEWAY
                flow.request.port = WS_PORT
    
    def response(self, flow: http.HTTPFlow):
        if flow.request.host in APP_DOMAINS:
            # TODO: Make CORS work without... this.
            flow.response.headers["Access-Control-Allow-Origin"] = "*"
            flow.response.headers["Content-security-policy"] = "default-src *  data: blob: filesystem: about: ws: wss: 'unsafe-inline' 'unsafe-eval'; script-src * data: blob: 'unsafe-inline' 'unsafe-eval'; connect-src * data: blob: 'unsafe-inline'; img-src * data: blob: 'unsafe-inline'; frame-src * data: blob: ; style-src * data: blob: 'unsafe-inline'; font-src * data: blob: 'unsafe-inline';"
            
            try:
                flow.response.headers["Access-Control-Allow-Headers"] = flow.request.headers["Access-Control-Allow-Headers"]
            except KeyError:
                flow.response.headers["Access-Control-Allow-Headers"] = "*"
            try:
                flow.response.headers["Access-Control-Allow-Methods"] = flow.request.headers["Access-Control-Allow-Methods"]
            except KeyError:
                flow.response.headers["Access-Control-Allow-Methods"] = "*"

addons = [
    ChatAppProxy()
]
