import re, spacy, json
from logging_config import logger

nlp = spacy.blank("en")
from spacy.matcher import PhraseMatcher

CANON = {
    "huhn": "chicken",
    "hühnerfleisch": "chicken",
    "truthahn": "turkey",
    "seealgenmehl": "kelp",
    "möhrchen": "carrot",
}

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
for k in CANON:
    matcher.add(k, [nlp.make_doc(k)])

def split_ingredients(text: str) -> list[str]:
    text = re.sub(r"\s*\([\w\s,%-]+\)", "", text)
    parts = re.split(r"[,%•;]", text)
    return [p.strip().lower() for p in parts if p.strip()]

def canonicalise(text: str) -> list[str]:
    logger.debug(f"Canonicalising ingredients: {text}")
    docs = [nlp(t) for t in split_ingredients(text)]
    output = []
    for doc in docs:
        matched = False
        for _, start, end in matcher(doc):
            term = doc[start:end].text.lower()
            output.append(CANON[term])
            matched = True
            break
        if not matched:
            output.append(doc.text)
    logger.debug(f"Canonical result: {output}")
    return output

if __name__ == "__main__":
    raw = "Hühnerfleisch, Lachsöl 1%, Cranberries, Seealgenmehl"
    logger.info(f"Testing canonicalise with: {raw}")
    print(json.dumps(canonicalise(raw), indent=2, ensure_ascii=False))
