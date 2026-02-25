from app.services.document_parser import DocumentParser

def test_sentence_split():
    cv_text = "I built ML models in Python. Led a team of 5 engineers."
    parser = DocumentParser(cv_text)
    sentences = parser.split_sentences()
    assert sentences == ["i built ml models in python", "led a team of 5 engineers"]

def test_keyword_extraction():
    cv_text = "Python Python SQL ML ML ML"
    parser = DocumentParser(cv_text)
    keywords = parser.extract_keywords()
    # Top 2 keywords should be ML and Python
    assert keywords[:2] == ["ml", "python"]