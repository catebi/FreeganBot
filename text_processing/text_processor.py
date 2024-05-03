from utils.lemmatizer import Lemmatizer
from utils.yaml_processor import YamlProcessor


def process_text_and_extract_keywords(text):
    lemmatizer = Lemmatizer()
    lemmas = lemmatizer.lemmatize(text + ' ' + text.replace('-', ''))
    matched_keywords = find_intersections(lemmas)
    return lemmas, matched_keywords


def find_intersections(lemmas: set) -> set[set]:
    matched_keywords = set()
    for group in YamlProcessor.groups_data():
        intersection_keywords = lemmas.intersection(group.keywords)
        intersection_include = lemmas.intersection(group.include_keywords)
        intersection_exclude = lemmas.intersection(group.exclude_keywords)

        if intersection_keywords:
            if (group.include_keywords and intersection_include) or (
                    group.exclude_keywords and not intersection_exclude):
                matched_keywords.update(intersection_keywords)
    return matched_keywords
