from copy import deepcopy

import pytest


class TestContext:
    def test_default_value(self, test_context):
        # Setting is missing
        with pytest.raises(AttributeError):
            test_context.foo

        # setdefault() returns the new value
        assert test_context.setdefault("foo", 23) == 23

        # setdefault() returns the existing value
        assert test_context.setdefault("foo", 45) == 23

        # Attribute access works
        assert test_context.foo == 23

    def test_deepcopy(self, session_context):
        """Paths are preserved through deepcopy()."""
        ld = session_context.local_data

        c = deepcopy(session_context)

        assert ld == c.local_data

    def test_get_cache_path(self, pytestconfig, test_context):
        """cache_path() returns the expected output."""
        base = test_context.local_data

        assert base.joinpath(
            "cache", "pytest", "bar.pkl"
        ) == test_context.get_cache_path("pytest", "bar.pkl")

    # Deprecated methods and attributes

    def test_load_config(self, test_context):
        # Calling this method is deprecated
        with pytest.deprecated_call():
            # Config files can be loaded and are parsed from YAML into Python objects
            assert isinstance(test_context.load_config("level"), dict)

        # The loaded file is stored and can be reused
        assert isinstance(test_context["level"], dict)

    def test_units(self, test_context):
        """Context.units can be used to parse units that are not standard in pint.

        i.e. message_data unit definitions are used.
        """
        with pytest.deprecated_call():
            assert test_context.units("15 USD_2005 / year").dimensionality == {
                "[currency]": 1,
                "[time]": -1,
            }
