#!/usr/bin/env python3
"""Unittests for the GithubOrgClient._public_repos_url method."""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the correct value
        from the mocked org property.
        """
        # Define mocked payload
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        client = GithubOrgClient("test_org")
        result = client._public_repos_url

        # Assert the private property returns the expected URL
        self.assertEqual(result, "https://api.github.com/orgs/test_org/repos")


if __name__ == "__main__":
    unittest.main()
