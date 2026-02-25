# app/services/document_parser.py

import re

class DocumentParser:
    """
    Simple text parser for CVs and Job Descriptions.
    Extracts sentences and keywords for downstream scoring.
    This will be updated later for .pdf and .docx files
    """
    
    def __init__(self, text: str):
        self.text = text
        
    def clean_text(self):
        text = self.text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return " ".join(text.strip().split())
    
    def split_sentences(self):
        sentences = self.text.lower().split(".")
        return [
            re.sub(r"[^\w\s]", "", s).strip()
            for s in sentences
            if s.strip()
        ]
    
    def extract_keywords(self):
        stopwords = {"and", "or", "the", "a", "an", "of", "in", "on", "for", "to"}
        words = self.clean_text().split()
        freq = {}
        for w in words:
            if w not in stopwords:
                freq[w] = freq.get(w, 0) + 1

        return sorted(freq, key=lambda w: (-freq[w], w))[:10]