#!/usr/bin/env python3
"""
Secure, reusable Jira Cloud API client using Bearer authentication
via the Atlassian API gateway (https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/).

Reads configuration from environment variables:
- JIRA_BASE_URL: e.g., https://anub131091.atlassian.net
- JIRA_EMAIL: Atlassian account email
- JIRA_API_TOKEN: Scoped Jira API token
- JIRA_CLOUD_ID: Atlassian Cloud ID (required for API gateway)

Does NOT print, expose, or hardcode the API token.
Does NOT make any API requests until explicitly called.
"""

import os
import sys
import requests
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin


class JiraClient:
    """Jira Cloud REST API client using Bearer token authentication via Atlassian API gateway."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
        cloud_id: Optional[str] = None,
    ):
        """
        Initialize Jira client.

        Args:
            base_url: Jira base URL (e.g., https://anub131091.atlassian.net).
                      If None, reads from JIRA_BASE_URL env var.
            email: Atlassian account email. If None, reads from JIRA_EMAIL env var.
            api_token: Scoped Jira API token. If None, reads from JIRA_API_TOKEN env var.
            cloud_id: Atlassian Cloud ID. If None, reads from JIRA_CLOUD_ID env var.

        Raises:
            ValueError: If required credentials are not provided.
        """
        self.base_url = base_url or os.environ.get("JIRA_BASE_URL")
        self.email = email or os.environ.get("JIRA_EMAIL")
        self.api_token = api_token or os.environ.get("JIRA_API_TOKEN")
        self.cloud_id = cloud_id or os.environ.get("JIRA_CLOUD_ID")

        # Validate required configuration
        missing = []
        if not self.base_url:
            missing.append("JIRA_BASE_URL")
        if not self.email:
            missing.append("JIRA_EMAIL")
        if not self.api_token:
            missing.append("JIRA_API_TOKEN")
        if not self.cloud_id:
            missing.append("JIRA_CLOUD_ID")

        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}. "
                f"Set these environment variables or pass as parameters."
            )

        # Normalize base URL
        self.base_url = self.base_url.rstrip("/")

        # Build API gateway base URL
        self._api_base = f"https://api.atlassian.com/ex/jira/{self.cloud_id}/rest/api/3"

        # Session with Bearer auth
        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        })

    @property
    def api_base(self) -> str:
        """Get the API base URL."""
        return self._api_base

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make an authenticated request to the Jira REST API via Atlassian gateway.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path (e.g., "/issue", "/project")
            params: Query parameters
            json: JSON body for POST/PUT
            **kwargs: Additional arguments passed to requests.request

        Returns:
            Response object

        Raises:
            requests.HTTPError: For HTTP error responses
            ValueError: If client not properly configured
        """
        if not self._session:
            raise ValueError("Client not initialized - missing configuration")

        url = urljoin(self.api_base + "/", endpoint.lstrip("/"))
        response = self._session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            **kwargs
        )
        return response

    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """GET request."""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: Optional[Dict] = None, params: Optional[Dict] = None) -> requests.Response:
        """POST request."""
        return self._request("POST", endpoint, json=json, params=params)

    def put(self, endpoint: str, json: Optional[Dict] = None) -> requests.Response:
        """PUT request."""
        return self._request("PUT", endpoint, json=json)

    def delete(self, endpoint: str) -> requests.Response:
        """DELETE request."""
        return self._request("DELETE", endpoint)

    # ============================================================
    # High-level API methods
    # ============================================================

    def test_connection(self) -> Dict[str, Any]:
        """
        Test the API connection and return current user info.
        Safe method - only reads current user, makes no changes.

        Returns:
            Dict with user info (displayName, emailAddress, accountId, etc.)

        Raises:
            requests.HTTPError: For HTTP error responses
        """
        response = self.get("/myself")
        response.raise_for_status()
        return response.json()

    def get_project(self, project_key: str) -> Dict[str, Any]:
        """Get project details by key."""
        response = self.get(f"/project/{project_key}")
        response.raise_for_status()
        return response.json()

    def search_projects(self, query: str = "", max_results: int = 50) -> List[Dict[str, Any]]:
        """Search for projects."""
        params = {"maxResults": max_results}
        if query:
            params["query"] = query
        response = self.get("/project/search", params=params)
        response.raise_for_status()
        return response.json().get("values", [])

    def create_project(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project."""
        response = self.post("/project", json=payload)
        response.raise_for_status()
        return response.json()

    def get_issue_types(self, project_key: str) -> List[Dict[str, Any]]:
        """Get issue types available for a project."""
        response = self.get("/issuetype/project", params={"projectKey": project_key})
        response.raise_for_status()
        return response.json()

    def create_issue(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new issue."""
        response = self.post("/issue", json={"fields": fields})
        response.raise_for_status()
        return response.json()

    def get_issue(self, issue_key: str, fields: Optional[str] = None) -> Dict[str, Any]:
        """Get issue details."""
        params = {}
        if fields:
            params["fields"] = fields
        response = self.get(f"/issue/{issue_key}", params=params)
        response.raise_for_status()
        return response.json()

    def update_issue(self, issue_key: str, fields: Dict[str, Any]) -> requests.Response:
        """Update an issue."""
        response = self.put(f"/issue/{issue_key}", json={"fields": fields})
        response.raise_for_status()
        return response

    def search_issues(
        self,
        jql: str,
        max_results: int = 50,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search issues using JQL."""
        params = {"jql": jql, "maxResults": max_results}
        if fields:
            params["fields"] = fields
        response = self.get("/search", params=params)
        response.raise_for_status()
        return response.json()

    def get_my_permissions(self, permissions: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get current user's permissions."""
        params = {}
        if permissions:
            params["permissions"] = ",".join(permissions)
        response = self.get("/mypermissions", params=params)
        response.raise_for_status()
        return response.json()


def create_client() -> JiraClient:
    """
    Factory function to create a JiraClient from environment variables.
    Raises ValueError with clear message if credentials missing.

    Returns:
        Configured JiraClient instance

    Raises:
        ValueError: If required environment variables are not set
    """
    return JiraClient()


def check_configuration() -> Dict[str, bool]:
    """
    Check which required environment variables are set without making API calls.

    Returns:
        Dict mapping variable names to boolean (True if set)
    """
    return {
        "JIRA_BASE_URL": bool(os.environ.get("JIRA_BASE_URL")),
        "JIRA_EMAIL": bool(os.environ.get("JIRA_EMAIL")),
        "JIRA_API_TOKEN": bool(os.environ.get("JIRA_API_TOKEN")),
        "JIRA_CLOUD_ID": bool(os.environ.get("JIRA_CLOUD_ID")),
    }


def get_missing_config() -> List[str]:
    """
    Get list of missing required environment variables.

    Returns:
        List of missing variable names
    """
    required = ["JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_CLOUD_ID"]
    return [var for var in required if not os.environ.get(var)]


# ============================================================
# CLI for configuration check (no API calls)
# ============================================================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Jira Cloud API Client - Configuration Check")
    parser.add_argument("--check", action="store_true", help="Check configuration only (no API calls)")
    parser.add_argument("--test", action="store_true", help="Test API connection (requires valid config)")
    args = parser.parse_args()

    if args.check or not (args.test):
        # Default: just check configuration
        print("Jira Client Configuration Check")
        print("=" * 40)

        config = check_configuration()
        missing = get_missing_config()

        for var, is_set in config.items():
            status = "✅ SET" if is_set else "❌ MISSING"
            print(f"  {var}: {status}")

        if missing:
            print(f"\nMissing: {', '.join(missing)}")
            print("\nSet these environment variables:")
            print("  JIRA_BASE_URL=https://anub131091.atlassian.net")
            print("  JIRA_EMAIL=your-email@example.com")
            print("  JIRA_API_TOKEN=your-api-token")
            print("  JIRA_CLOUD_ID=your-cloud-id")
            sys.exit(1)
        else:
            print("\n✅ All required configuration variables are set")
            if not args.test:
                sys.exit(0)

    if args.test:
        print("\nTesting API connection...")
        try:
            client = create_client()
            print(f"Base URL: {client.base_url}")
            print(f"Email: {client.email}")
            print(f"Cloud ID: {client.cloud_id}")
            print("API Token: [REDACTED]")
            print(f"API Base: {client.api_base}")

            user = client.test_connection()
            print(f"\n✅ Connected successfully!")
            print(f"   User: {user.get('displayName', user.get('emailAddress', 'Unknown'))}")
            print(f"   Account ID: {user.get('accountId')}")

        except ValueError as e:
            print(f"❌ Configuration error: {e}")
            sys.exit(1)
        except requests.HTTPError as e:
            print(f"❌ HTTP error: {e.response.status_code} - {e.response.text}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)