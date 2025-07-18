#!/usr/bin/env python3
"""Unittests for the GithubOrgClient.org method."""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"org": "Google"}),
        ("abc", {"org": "ABC"}),
    ])
    # NOTE: The patch path must match how get_json is imported in GithubOrgClient.
    # If GithubOrgClient does: from client import get_json, then patch 'client.get_json'.
    # If it does: from .utils import get_json, then patch 'utils.get_json'.
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test GithubOrgClient.org returns expected dictionary and calls get_json once."""
        # Setup the mock to return the expected payload
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        # Assert get_json called once with correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        # Assert the org property returns the mocked payload
        self.assertEqual(result, expected_payload)


if __name__ == "__main__":
    unittest.main()
