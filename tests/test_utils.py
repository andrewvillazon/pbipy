from pbipy import utils


def test_to_snake_case():
    assert(utils.to_snake_case("FluffyWuffy")) == "fluffy_wuffy"
    assert(utils.to_snake_case("webURL")) == "web_url"
    assert utils.to_snake_case("AyeBeeCee") == "aye_bee_cee"


def test_to_camel_case():
    assert(utils.to_camel_case("dataset_user_access_right")) == "datasetUserAccessRight"
    assert(utils.to_camel_case("identifier")) == "identifier"
    assert(utils.to_camel_case("principal_type")) == "principalType"