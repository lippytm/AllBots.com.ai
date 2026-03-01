"""
tests/test_integrations.py
Tests for the integrations package.
"""
import pytest

from integrations.web3_connector import Web3Connector
from integrations.cloud_connector import CloudConnector, SUPPORTED_PROVIDERS


class TestWeb3Connector:
    def test_connect_sets_connected_flag(self):
        conn = Web3Connector(rpc_url="http://localhost:8545")
        result = conn.connect()
        assert result is True
        assert conn._connected is True

    def test_call_contract_requires_connection(self):
        conn = Web3Connector()
        with pytest.raises(RuntimeError, match="Not connected"):
            conn.call_contract("0xABC", "balanceOf", [])

    def test_call_contract_after_connect(self):
        conn = Web3Connector()
        conn.connect()
        result = conn.call_contract("0xABC", "balanceOf", ["0x123"])
        assert result is None  # stub returns None

    def test_send_transaction_requires_connection(self):
        conn = Web3Connector()
        with pytest.raises(RuntimeError, match="Not connected"):
            conn.send_transaction({"to": "0xDEF", "value": 1})

    def test_send_transaction_returns_hash(self):
        conn = Web3Connector()
        conn.connect()
        tx_hash = conn.send_transaction({"to": "0xDEF", "value": 1})
        assert tx_hash.startswith("0x")


class TestCloudConnector:
    def test_supported_providers(self):
        for provider in SUPPORTED_PROVIDERS:
            conn = CloudConnector(provider=provider)
            assert conn.provider == provider

    def test_unsupported_provider_raises(self):
        with pytest.raises(ValueError, match="Unsupported provider"):
            CloudConnector(provider="oracle")

    def test_deploy_returns_descriptor(self):
        conn = CloudConnector(provider="aws", region="eu-west-1")
        desc = conn.deploy("my_bot", {"replicas": 3})
        assert desc["bot_name"] == "my_bot"
        assert desc["provider"] == "aws"
        assert desc["region"] == "eu-west-1"
        assert desc["status"] == "pending"

    def test_teardown_returns_true(self):
        conn = CloudConnector(provider="gcp")
        assert conn.teardown("deploy-001") is True
