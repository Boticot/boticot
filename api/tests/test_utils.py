from utils import check_entity_overlap


def test_should_remove_duckling_when_entities_overlap():
    entities = [{"value": "value1", "extractor": "CRFEntityExtractor", "start" : 1, "end": 6},
                {"value": "value2", "extractor": "CRFEntityExtractor", "start": 7, "end": 12},
                {"value": "demain", "extractor": "DucklingHTTPExtractor", "start": 8, "end": 13}]
    entities_without_duckling = [{"value": "value1", "extractor" : "CRFEntityExtractor", "start" : 1, "end": 6},
                                 {"value": "value2", "extractor": "CRFEntityExtractor", "start": 7, "end": 12}]
    duckling_entities = [{"value": "demain", "extractor": "DucklingHTTPExtractor", "start": 8, "end": 13}]
    assert check_entity_overlap(entities, duckling_entities) == entities_without_duckling


def test_should_not_remove_duckling_when_entities_do_not_overlap():
    entities = [{"value": "value1", "extractor": "CRFEntityExtractor", "start" : 1, "end": 6},
                {"value": "value2", "extractor": "CRFEntityExtractor", "start": 7, "end": 12},
                {"value": "demain", "extractor": "DucklingHTTPExtractor", "start": 14, "end": 19},
                {"value": "hier", "extractor": "DucklingHTTPExtractor", "start": 22, "end": 25}]
    duckling_entities = [{"value": "demain", "extractor": "DucklingHTTPExtractor", "start": 14, "end": 19},
                         {"value": "hier", "extractor": "DucklingHTTPExtractor", "start": 22, "end": 25}]
    assert check_entity_overlap(entities, duckling_entities) == entities
