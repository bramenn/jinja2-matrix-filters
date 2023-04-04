from jinja2 import Environment
import pytest


@pytest.fixture
def jinja2_env():
    return Environment(extensions=["jinja2_matrix_filters.MatrixFiltersExtension"])


FILTERS = {
    "user_bridge_info": {
        "params": "@mxwa_56123456789:example.com",
        "validate": "mxwa,56123456789",
    },
    "user_bridge_prefix": {
        "params": "@mxwa_56123456789:example.com",
        "validate": "mxwa",
    },
    "user_bridge_account_id": {
        "params": "@mxwa_56123456789:example.com",
        "validate": "56123456789",
    },
    "user_homeserver": {
        "params": "@mxwa_56123456789:example.com",
        "validate": "example.com",
    },
    "location_message_geo_uri": {
        "params": '{"geo_uri":"geo:39.4535975,-31.2655426"}',
        "validate": "geo:39.4535975,-31.2655426",
    },
    "location_message_latitude": {
        "params": '{"geo_uri":"geo:39.4535975,-31.2655426"}',
        "validate": "39.4535975",
    },
    "location_message_longitude": {
        "params": '{"geo_uri":"geo:39.4535975,-31.2655426"}',
        "validate": "-31.2655426",
    },
    "google_location_url": {
        "params": "geo:39.4535975,-31.2655426",
        "validate": "https://www.google.com/maps?q=39.4535975,-31.2655426",
    },
}


def test_extension_loads(jinja2_env: Environment):
    assert set(FILTERS.keys()).issubset(
        set(jinja2_env.filters.keys())
    ), "Missing filters from defined list"


@pytest.mark.parametrize("key,tests", FILTERS.items())
def test_filter_return_types(jinja2_env: Environment, key, tests):
    class DNE(object):
        pass

    if isinstance(tests, tuple):
        for test in tests:
            test_filter_return_types(jinja2_env, key, test)

    if "params" in tests:
        if isinstance(tests["params"], tuple):
            if "kwargs" in tests:
                rslt = jinja2_env.filters[key](*tests["params"], **tests["kwargs"])
            else:
                rslt = jinja2_env.filters[key](*tests["params"])
        else:
            if "kwargs" in tests:
                rslt = jinja2_env.filters[key](tests["params"], **tests["kwargs"])
            else:
                rslt = jinja2_env.filters[key](tests["params"])
    else:
        rslt = DNE

    if "validate" in tests:
        if rslt is not DNE:
            if hasattr(tests["validate"], "__call__"):
                assert tests["validate"](rslt)
            else:
                assert tests["validate"] == rslt
        elif hasattr(tests["validate"], "__call__"):
            assert tests["validate"](rslt)
        else:
            assert False, "No valid check for {}".format(key)


# def test_extension_collision(recwarn):
#     env = Environment()
#     env.filters["b64decode"] = lambda x: "test string"

#     env.add_extension("jinja2_matrix_filters.MatrixFiltersExtension")
#     warn = recwarn.pop()
#     assert isinstance(warn.message, RuntimeWarning), "Warning not thrown for collision"
