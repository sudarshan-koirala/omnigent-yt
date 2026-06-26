"""
Meridian Labs auth (STARTER, intentionally messy).

Everything is crammed into one file: OAuth exchange, JWT signing/verifying,
and in-memory session handling. This is the file Polly will refactor into
oauth.py, jwt_utils.py, and sessions.py, with tests for each.
"""
import time
import hmac
import hashlib
import base64
import json
import secrets

SECRET = "dev-only-secret-change-me"
USERS = {
    "jordan.lee@example.com": "pro",
    "amelia.ferraro@example.com": "enterprise",
}
SESSIONS = {}            # session_id -> {"email":..., "expires":...}
OAUTH_CLIENTS = {        # very fake oauth client registry
    "meridian-web": "web-secret",
    "meridian-cli": "cli-secret",
}


# --- JWT bits ---------------------------------------------------------
def _b64(raw):
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def sign_jwt(payload):
    header = {"alg": "HS256", "typ": "JWT"}
    h = _b64(json.dumps(header).encode())
    p = _b64(json.dumps(payload).encode())
    signing_input = f"{h}.{p}".encode()
    sig = hmac.new(SECRET.encode(), signing_input, hashlib.sha256).digest()
    return f"{h}.{p}.{_b64(sig)}"


def verify_jwt(token):
    try:
        h, p, s = token.split(".")
    except ValueError:
        return None
    signing_input = f"{h}.{p}".encode()
    expected = hmac.new(SECRET.encode(), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(_b64(expected), s):
        return None
    pad = "=" * (-len(p) % 4)
    payload = json.loads(base64.urlsafe_b64decode(p + pad))
    if payload.get("exp", 0) < time.time():
        return None
    return payload


# --- OAuth bits -------------------------------------------------------
def oauth_token(client_id, client_secret):
    if OAUTH_CLIENTS.get(client_id) != client_secret:
        return None
    return sign_jwt({"client": client_id, "exp": time.time() + 3600})


# --- Session bits -----------------------------------------------------
def create_session(email):
    sid = secrets.token_hex(16)
    SESSIONS[sid] = {"email": email, "expires": time.time() + 1800}
    return sid


def read_session(sid):
    s = SESSIONS.get(sid)
    if not s or s["expires"] < time.time():
        return None
    return s["email"]


# --- Public API the app calls ----------------------------------------
def login(email, password):
    # password check is fake on purpose for the demo
    if email not in USERS or not password:
        return None
    return sign_jwt({"email": email, "tier": USERS[email],
                     "exp": time.time() + 3600})


def verify(token):
    payload = verify_jwt(token)
    if not payload:
        return None
    return {"email": payload.get("email"), "tier": payload.get("tier")}
