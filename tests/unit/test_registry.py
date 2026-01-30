from src.adapters.registry.registry_adapter import ConfigRegistry
from tests.fixtures.fake_adapter import FakeAdapter


def test_registry_resolves_adapter():
    config = {
        "registries": {"sources": {"fake": "tests.fixtures.fake_adapter.FakeAdapter"}},
        "adapters": {"fake": {"x": 1}},
    }

    registry = ConfigRegistry(config)
    adapter = registry.resolve("sources", "fake")

    assert isinstance(adapter, FakeAdapter)
    assert adapter.config == {"x": 1}
