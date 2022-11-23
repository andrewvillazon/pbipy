from pbipy import utils


def test_camel_to_snake():
    assert utils.camel_to_snake("AyeBeeCee") == "aye_bee_cee"
    assert utils.camel_to_snake("webURL") == "web_url"
    assert utils.camel_to_snake("addRowsAPIEnabled") == "add_rows_api_enabled"


def test_camel_case_dict_keys_converts_keys():

    test_dict = utils.camel_case_dict_keys(
        {
            "FluffyWuffy": None,
            "webURL": None,
        }
    )

    expected_dict = {
        "fluffy_wuffy": None,
        "web_url": None,
    }
    
    assert test_dict == expected_dict
