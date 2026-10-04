#!/usr/bin/env python3
"""Connect Codex to a LibreAgent MCP server from a remote computer (SSH, no local browser).

Codex's own login waits for a browser redirect to 127.0.0.1 on the computer that runs Codex,
which never arrives when the browser is on another device. This tool splits the login in two
steps that survive between sessions:

  codex-mcp-login-remote.py start  [--name libreagent] [--url https://server/mcp]
      prints the address to open in any browser signed in to LibreAgent;
  codex-mcp-login-remote.py finish <address shown by the browser after approval>
      exchanges the code and stores the connection where Codex reads it.

Only Codex's file credential store (mcp_oauth_credentials_store = "file") is written. With the
keyring store, run "codex mcp login <name>" from a session that can open the keychain.
"""
import base64
import hashlib
import json
import os
import secrets
import subprocess
import sys
import time
import tomllib
import urllib.parse
import urllib.request
from pathlib import Path

CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
STATE = CODEX_HOME / "libreagent-remote-login.json"
REDIRECT = "http://127.0.0.1:1455/callback"


def fail(message):
    print(f"Erreur : {message}", file=sys.stderr)
    sys.exit(1)


def http_json(url, data=None, form=False):
    headers = {"Accept": "application/json"}
    body = None
    if data is not None:
        if form:
            body = urllib.parse.urlencode(data).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        fail(f"{url} a répondu {error.code} : {error.read().decode(errors='replace')[:300]}")
    except urllib.error.URLError as error:
        fail(f"{url} est injoignable : {error.reason}")


def server_url(name, explicit):
    if explicit:
        return explicit
    found = subprocess.run(["codex", "mcp", "get", name, "--json"], capture_output=True, text=True)
    if found.returncode == 0:
        try:
            value = json.loads(found.stdout)
            url = value.get("url") or value.get("transport", {}).get("url")
            if url:
                return url
        except ValueError:
            pass
    fail(f"adresse du serveur MCP « {name} » introuvable dans Codex ; passez --url https://serveur/mcp.")


def store_key(name, url):
    # Same key as Codex: server name and the first 16 hex digits of the SHA-256 of its transport.
    digest = hashlib.sha256(json.dumps({"type": "http", "url": url, "headers": {}}, separators=(",", ":")).encode())
    return f"{name}|{digest.hexdigest()[:16]}"


def credentials_store():
    config = CODEX_HOME / "config.toml"
    if not config.exists():
        return "auto"
    return tomllib.loads(config.read_text()).get("mcp_oauth_credentials_store", "auto")


def start(args):
    name = args.get("--name", "libreagent")
    url = server_url(name, args.get("--url"))
    resource = url
    origin = urllib.parse.urlsplit(url)
    metadata = http_json(f"{origin.scheme}://{origin.netloc}/.well-known/oauth-authorization-server")
    client = http_json(metadata["registration_endpoint"], {
        "client_name": "Codex (ordinateur distant)",
        "redirect_uris": [REDIRECT],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
    })
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(18)
    CODEX_HOME.mkdir(parents=True, exist_ok=True)
    payload = {"name": name, "url": url, "resource": resource, "issuer": metadata["issuer"],
               "token_endpoint": metadata["token_endpoint"], "client_id": client["client_id"],
               "verifier": verifier, "state": state, "created_at": time.time()}
    STATE.write_text(json.dumps(payload))
    STATE.chmod(0o600)
    query = urllib.parse.urlencode({
        "response_type": "code", "client_id": client["client_id"], "state": state,
        "code_challenge": challenge, "code_challenge_method": "S256", "redirect_uri": REDIRECT,
        "scope": "mcp:access", "resource": resource,
    })
    print("Ouvrez cette adresse dans un navigateur connecté à LibreAgent et autorisez Codex :")
    print(f"{metadata['authorization_endpoint']}?{query}")
    print("Le navigateur finit sur une page 127.0.0.1 introuvable : copiez son adresse complète, puis lancez")
    print(f"  {Path(sys.argv[0]).name} finish '<adresse copiée>'")


def finish(callback):
    if not STATE.exists():
        fail("aucune connexion en cours : lancez d'abord « start ».")
    saved = json.loads(STATE.read_text())
    if time.time() - saved["created_at"] > 3600:
        fail("cette demande a plus d'une heure : relancez « start ».")
    params = urllib.parse.parse_qs(urllib.parse.urlsplit(callback.strip()).query)
    if "error" in params:
        fail(f"LibreAgent a refusé l'autorisation : {params['error'][0]}")
    if params.get("state", [None])[0] != saved["state"]:
        fail("cette adresse ne correspond pas à la dernière demande : relancez « start ».")
    code = params.get("code", [None])[0] or fail("l'adresse ne contient pas de code d'autorisation.")
    mode = credentials_store()
    if mode != "file":
        fail(f"Codex range ses connexions MCP dans « {mode} », pas dans un fichier : lancez « codex mcp login {saved['name']} » depuis une session qui peut ouvrir le trousseau.")
    tokens = http_json(saved["token_endpoint"], {
        "grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT,
        "client_id": saved["client_id"], "code_verifier": saved["verifier"], "resource": saved["resource"],
    }, form=True)
    path = CODEX_HOME / ".credentials.json"
    current = json.loads(path.read_text()) if path.exists() else {}
    current[store_key(saved["name"], saved["url"])] = {
        "server_name": saved["name"], "server_url": saved["url"], "issuer": saved["issuer"],
        "client_id": saved["client_id"], "access_token": tokens["access_token"],
        "expires_at": int((time.time() + int(tokens.get("expires_in", 3600))) * 1000),
        "refresh_token": tokens.get("refresh_token"), "scopes": tokens.get("scope", "mcp:access").split(),
    }
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(current))
    temporary.chmod(0o600)
    temporary.replace(path)
    STATE.unlink()
    print(f"Codex est connecté à {saved['url']}. Vérifiez avec « codex mcp list ».")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in {"start", "finish"}:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "finish":
        if len(sys.argv) != 3:
            fail("donnez l'adresse affichée par le navigateur après l'autorisation.")
        finish(sys.argv[2])
    else:
        rest = sys.argv[2:]
        start(dict(zip(rest[::2], rest[1::2])))


if __name__ == "__main__":
    main()
