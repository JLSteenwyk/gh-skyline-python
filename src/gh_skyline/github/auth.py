"""gh-backed auth adapter for host/token/graphql behavior parity."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request

from gh_skyline.core.errors import ErrorType, new_error


class GhAuthAdapter:
    """Adapter that delegates auth and GraphQL calls to gh CLI."""

    def __init__(self, gh_bin: str = "gh") -> None:
        self.gh_bin = gh_bin
        self._gh_available = shutil.which(self.gh_bin) is not None

    def default_host(self) -> str:
        """Get default GitHub host from gh auth status JSON or env fallback."""
        host_from_env = os.environ.get("GH_HOST")
        if host_from_env:
            return host_from_env

        if not self._gh_available:
            return "github.com"

        cmd = [self.gh_bin, "auth", "status", "--json", "hosts"]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
            payload = json.loads(proc.stdout or "{}")
        except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
            raise new_error(ErrorType.NETWORK, "failed to resolve default host via gh", exc)

        hosts = payload.get("hosts", {})
        if not isinstance(hosts, dict) or len(hosts) == 0:
            return "github.com"

        return next(iter(hosts.keys()))

    def auth_token(self) -> str:
        """Get auth token from env or gh."""
        env_token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if env_token:
            return env_token

        if not self._gh_available:
            raise new_error(
                ErrorType.NETWORK,
                "gh CLI not found. Install gh or set GITHUB_TOKEN/GH_TOKEN",
                None,
            )

        cmd = [self.gh_bin, "auth", "token"]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as exc:
            raise new_error(ErrorType.NETWORK, "failed to retrieve gh auth token", exc)

        token = proc.stdout.strip()
        if not token:
            raise new_error(ErrorType.VALIDATION, "gh auth token returned empty token", None)
        return token

    def graphql(self, query: str, variables: dict[str, object] | None = None) -> dict[str, object]:
        """Execute GraphQL query via gh api graphql or direct HTTPS fallback."""
        if not self._gh_available:
            return self._graphql_via_https(query, variables or {})

        cmd = [self.gh_bin, "api", "graphql", "-f", f"query={query}"]
        for key, value in (variables or {}).items():
            cmd.extend(["-f", f"{key}={value}"])

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
            payload = json.loads(proc.stdout or "{}")
        except subprocess.CalledProcessError as exc:
            raise new_error(ErrorType.GRAPHQL, "failed graphql request via gh", exc)
        except json.JSONDecodeError as exc:
            raise new_error(ErrorType.GRAPHQL, "invalid graphql JSON response from gh", exc)

        return payload

    def _graphql_via_https(self, query: str, variables: dict[str, object]) -> dict[str, object]:
        """Call GraphQL endpoint directly using bearer token."""
        host = self.default_host()
        token = self.auth_token()

        if host == "github.com":
            url = "https://api.github.com/graphql"
        else:
            url = f"https://{host}/api/graphql"
        body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "gh-skyline-python",
        }
        req = urllib.request.Request(url=url, data=body, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req) as resp:  # noqa: S310
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            details = ""
            try:
                details = exc.read().decode("utf-8")
            except Exception:
                details = ""
            message = "failed graphql request via HTTPS"
            if details:
                message = f"{message}: {details}"
            raise new_error(ErrorType.GRAPHQL, message, exc)
        except urllib.error.URLError as exc:
            raise new_error(ErrorType.GRAPHQL, "failed graphql request via HTTPS", exc)
        except json.JSONDecodeError as exc:
            raise new_error(ErrorType.GRAPHQL, "invalid graphql JSON response", exc)

        return payload
