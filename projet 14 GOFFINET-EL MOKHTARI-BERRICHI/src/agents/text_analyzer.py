import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import Tuple

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from src.models import ExtractedData

load_dotenv()

class TextAnalyzerAgentOnline:
    """Agent d'analyse de texte utilisant directement l'API OpenAI"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ La variable OPENAI_API_KEY n'est pas définie.")
        
        self.client = OpenAI(api_key=api_key)

        # Prompts
        self.classification_prompt = """
Analysez le texte suivant et déterminez s'il s'agit d'informations pour créer un CV, une facture, ou un rapport.

Règles de classification:
- CV: contient des informations personnelles, expériences professionnelles, formations, compétences
- Facture: contient des informations de facturation, services/produits, montants, dates
- Rapport: contient un titre, des sections, des analyses, des conclusions

Texte à analyser:
{{$input}}

Répondez avec un seul mot: CV, FACTURE, ou RAPPORT
Ajoutez aussi un score de confiance entre 0 et 1.

Format de réponse: TYPE|SCORE
"""

        self.extraction_prompt = """
Extrayez les informations structurées du texte suivant pour créer un {{$document_type}}.

Texte d'entrée:
{{$input}}

Pour un CV, extrayez:
- nom (obligatoire)
- email, téléphone, adresse (si disponibles)
- expériences professionnelles (liste)
- formations (liste)
- compétences (liste)

Pour une FACTURE, extrayez:
- numéro de facture
- date d'émission et date d'échéance
- nom du client
- adresse du client
- nom et adresse du fournisseur
- email du fournisseur
- liste des services/produits/prestations avec quantité et prix
- montant total HT
- TVA
- montant total TTC
- conditions de paiement
- mentions légales
- remarques

Pour un RAPPORT, extrayez:
- titre
- auteur
- date
- résumé
- sections avec titres et contenu
- conclusions

Répondez au format JSON structuré selon le type de document.
"""

    def _call_openai(self, prompt: str) -> str:
        """Appel synchronisé à l'API OpenAI"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def classify_document_type(self, text: str) -> Tuple[str, float]:
        """Classification en ligne via OpenAI"""
        prompt = self.classification_prompt.replace("{{$input}}", text)
        response = self._call_openai(prompt)

        if "|" in response:
            doc_type, score_str = response.split("|", 1)
            doc_type = doc_type.strip().lower()
            try:
                score = float(score_str.strip())
            except ValueError:
                score = 0.5
        else:
            doc_type = response.lower()
            score = 0.5

        if doc_type in ["cv", "curriculum", "resume"]:
            return "cv", score
        elif doc_type in ["facture", "invoice", "bill"]:
            return "facture", score
        elif doc_type in ["rapport", "report"]:
            return "rapport", score
        else:
            return "rapport", 0.3  # Par défaut

    def extract_structured_data(self, text: str, document_type: str) -> dict:
        prompt = self.extraction_prompt.replace("{{$input}}", text)
        prompt = prompt.replace("{{$document_type}}", document_type.upper())
        response = self._call_openai(prompt)
        print("\n=== 🔍 Réponse OpenAI ===")
        print(response)
        print("=========================\n")

        try:
            data = json.loads(response)
            # Si le JSON est du type {"CV": {...}} ou {"FACTURE": {...}}, on déplie
            if isinstance(data, dict) and len(data) == 1:
                key = list(data.keys())[0]
                if isinstance(data[key], dict):
                    data = data[key]
            return data
        except json.JSONDecodeError:
            return {"raw_response": response, "extraction_method": "fallback"}

    async def analyze_text(self, text: str) -> ExtractedData:
        """Analyse complète: classification + extraction"""
        doc_type, confidence = self.classify_document_type(text)
        extracted_dict = self.extract_structured_data(text, doc_type)

        return ExtractedData(
            document_type=doc_type,
            confidence_score=confidence,
            data=extracted_dict,
            raw_text=text
        )
