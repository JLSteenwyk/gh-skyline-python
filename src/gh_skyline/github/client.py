"""GitHub client that mirrors key Go GraphQL behavior."""

from __future__ import annotations

from gh_skyline.core.errors import ErrorType, new_error
from gh_skyline.github.auth import GhAuthAdapter


class GitHubClient:
    """GraphQL client wrapper using GhAuthAdapter."""

    def __init__(self, auth_adapter: GhAuthAdapter | None = None) -> None:
        self.auth = auth_adapter or GhAuthAdapter()

    def get_authenticated_user(self) -> str:
        query = """
        query {
            viewer {
                login
            }
        }
        """
        payload = self.auth.graphql(query)
        login = payload.get("data", {}).get("viewer", {}).get("login", "")
        if not isinstance(login, str) or not login:
            raise new_error(ErrorType.VALIDATION, "received empty username from GitHub API", None)
        return login

    def fetch_contributions(self, username: str, year: int) -> dict[str, object]:
        """Fetch contribution calendar for a username/year."""
        if not username:
            raise new_error(ErrorType.VALIDATION, "username cannot be empty", None)

        if year < 2008:
            raise new_error(ErrorType.VALIDATION, "year cannot be before GitHub's launch (2008)", None)

        start_date = f"{year}-01-01T00:00:00Z"
        end_date = f"{year}-12-31T23:59:59Z"

        query = """
        query ContributionGraph($username: String!, $from: DateTime!, $to: DateTime!) {
            user(login: $username) {
                login
                contributionsCollection(from: $from, to: $to) {
                    contributionCalendar {
                        totalContributions
                        weeks {
                            contributionDays {
                                contributionCount
                                date
                            }
                        }
                    }
                }
            }
        }
        """

        payload = self.auth.graphql(
            query,
            {
                "username": username,
                "from": start_date,
                "to": end_date,
            },
        )
        login = payload.get("data", {}).get("user", {}).get("login", "")
        if not isinstance(login, str) or not login:
            raise new_error(ErrorType.VALIDATION, "received empty username from GitHub API", None)

        return payload

    def get_user_join_year(self, username: str) -> int:
        if not username:
            raise new_error(ErrorType.VALIDATION, "username cannot be empty", None)

        query = """
        query UserJoinDate($username: String!) {
            user(login: $username) {
                createdAt
            }
        }
        """
        payload = self.auth.graphql(query, {"username": username})
        created_at = payload.get("data", {}).get("user", {}).get("createdAt", "")
        if not isinstance(created_at, str) or len(created_at) < 4:
            raise new_error(ErrorType.VALIDATION, "invalid join date received from GitHub API", None)

        try:
            return int(created_at[:4])
        except ValueError as exc:
            raise new_error(ErrorType.VALIDATION, "invalid join date received from GitHub API", exc)
