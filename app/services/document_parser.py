# app/services/document_parser.py

import re
from collections import Counter

class DocumentParser:
    """
    Parses a document (CV or Job Description) into:
        - Sentences: cleaned
        - Keywords: cleaned single and multi-word terms
    """
    
    DEFAULT_STOPWORDS = {
        "and", "or", "the", "a", "an", "of", "in", "on", "for", "to",
        "with", "by", "at", "from", "as", "is", "are", "be",
        "responsible", "experience", "work", "team", "company",
        "role", "position", "requirements", "skills", "candidate",
        "applicant", "opportunity", "environment", "managed", "led",
    }
    
    ABBREVIATIONS = {
        "ml": "machine learning",
        "nlp": "natural language processing",
        "dl": "deep learning",
        "js": "javascript",
        "aws": "amazon web services",
    }
    
    def __init__(self, text: str):
        self.raw_text = text
        self.cleaned_text = self._clean_text(text)
        
    def _clean_text(self, text: str) -> str:
        """
        Lowercase and normalise whitespace.
        Keep common tech symbols (+, *, ., /) for skills like C++, Node.js, CI/CD   
        """
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s\+\#\./]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    
    def extract_sentences(self):
        """
        Splits text into sentences, cleaning each.
        Splits on ., !, ?, or line breaks.
        """
        # Split on ., !, ?, or newLine
        raw_sentences = re.split(r"[.!?\n]", self.raw_text)
        sentences = [
            s.strip().lower() for s in raw_sentences
            if s.strip()
        ]
        return sentences
    
    def extract_keywords(self, top_n=20, custom_stopwords=None):
        """
        Returns top_n keywords (single + multi-word bigrams) from docs
        """ 
        stopwords = self.DEFAULT_STOPWORDS.copy()
        if custom_stopwords:
            stopwords.update(custom_stopwords)
            
        tokens = self.cleaned_text.split()
        
        tokens = [self.ABBREVIATIONS.get(t, t) for t in tokens]
        
        # Remove stopwords and very short tokens
        tokens = [t for t in tokens if t not in stopwords and len(t) > 2]
        
        # Single word frequencies
        word_freq = Counter(tokens)
        
        # Extracts bigrams (2-word phrases) for skills like 'machine learning'
        bigrams = [
            f"{tokens[i]} {tokens[i+1]}"
            for i in range(len(tokens)-1)
            if tokens[i] not in stopwords and tokens[i+1] not in stopwords
        ]
        bigram_freq = Counter(bigrams)
        
        # Combine single words and bigrams
        combined = word_freq + bigram_freq
        
        return [k for k, _ in combined.most_common(top_n)]