"""
Agent Générateur de Structure - Transforme les données extraites en structure de document
"""
from typing import Dict, Any, Optional
from datetime import datetime
import json
from ..models import CVData, FactureData, RapportData, ExtractedData

class StructureGeneratorAgent:
    """Agent responsable de la transformation des données extraites en structure de document"""
    
    def __init__(self):
        pass
    
    def generate_structure(self, extracted_data: ExtractedData) -> Any:
        """
        Génère la structure appropriée en fonction du type de document
        
        Args:
            extracted_data: Données extraites du texte
            
        Returns:
            Objet structuré (CVData, FactureData, ou RapportData)
        """
        if extracted_data.document_type == "cv":
            return self._generate_cv_structure(extracted_data.data)
        elif extracted_data.document_type == "facture":
            return self._generate_invoice_structure(extracted_data.data)
        elif extracted_data.document_type == "rapport":
            return self._generate_report_structure(extracted_data.data)
        else:
            # Par défaut, générer un rapport
            return self._generate_report_structure(extracted_data.data)
    
    def _generate_cv_structure(self, raw_data: Dict[str, Any]) -> CVData:
        """Génère la structure pour un CV"""
        try:
            # Extraire les informations de base
            nom = raw_data.get("nom", "Nom non spécifié")
            
            # Extraire les informations de contact
            email = raw_data.get("email")
            telephone = raw_data.get("telephone")
            adresse = raw_data.get("adresse")
            
            # Extraire le poste
            poste = raw_data.get("poste")
            if not poste:
                # Vérifier les variations possibles
                for key in ["poste", "Poste", "POSTE", "position", "Position", "POSITION"]:
                    if key in raw_data:
                        poste = raw_data[key]
                        break
            
            # Extraire les expériences professionnelles
            experiences = []
            if "experiences" in raw_data:
                experiences = [exp for exp in raw_data["experiences"] if exp and exp.strip()]
            elif "experience" in raw_data:
                experiences = [exp for exp in raw_data["experience"] if exp and exp.strip()]
            elif "experiences_professionnelles" in raw_data:
                experiences = [exp for exp in raw_data["experiences_professionnelles"] if exp and exp.strip()]
            elif "expériences" in raw_data:
                experiences = [exp for exp in raw_data["expériences"] if exp and exp.strip()]
            elif "expérience" in raw_data:
                experiences = [exp for exp in raw_data["expérience"] if exp and exp.strip()]
            elif "expériences_professionnelles" in raw_data:
                experiences = [exp for exp in raw_data["expériences_professionnelles"] if exp and exp.strip()]
                
            # Extraire les formations
            formations = []
            if "formations" in raw_data:
                formations = [form for form in raw_data["formations"] if form and form.strip()]
            elif "formation" in raw_data:
                formations = [form for form in raw_data["formation"] if form and form.strip()]
            elif "formations_academiques" in raw_data:
                formations = [form for form in raw_data["formations_academiques"] if form and form.strip()]
            elif "formations" in raw_data:
                formations = [form for form in raw_data["formations"] if form and form.strip()]
            elif "formation" in raw_data:
                formations = [form for form in raw_data["formation"] if form and form.strip()]
            elif "formations_academiques" in raw_data:
                formations = [form for form in raw_data["formations_academiques"] if form and form.strip()]
                
            # Extraire les compétences
            competences = []
            if "competences" in raw_data:
                competences = [comp for comp in raw_data["competences"] if comp and comp.strip()]
            elif "competence" in raw_data:
                competences = [comp for comp in raw_data["competence"] if comp and comp.strip()]
            elif "skills" in raw_data:
                competences = [comp for comp in raw_data["skills"] if comp and comp.strip()]
            elif "compétences" in raw_data:
                competences = [comp for comp in raw_data["compétences"] if comp and comp.strip()]
            elif "compétence" in raw_data:
                competences = [comp for comp in raw_data["compétence"] if comp and comp.strip()]
                
            return CVData(
                nom=nom,
                email=email,
                telephone=telephone,
                adresse=adresse,
                experiences=experiences,
                formations=formations,
                competences=competences,
                poste=poste
            )
            
        except Exception as e:
            print(f"Erreur lors de la génération de la structure CV: {e}")
            # Retourner une structure minimale
            return CVData(nom="Nom non spécifié")
    
    def _generate_invoice_structure(self, raw_data: Dict[str, Any]) -> FactureData:
        """Génère la structure pour une facture"""
        try:
            # Extraire les informations de base
            numero_facture = raw_data.get("numero_facture", "FACT-001")
            
            # Extraire la date
            date_str = raw_data.get("date")
            if date_str:
                try:
                    date = datetime.fromisoformat(date_str)
                except:
                    date = datetime.now()
            else:
                date = datetime.now()
                
            # Extraire les informations du client
            client_nom = raw_data.get("client_nom", "Client non spécifié")
            client_adresse = raw_data.get("client_adresse")
            
            # Extraire les services
            services = []
            if "services" in raw_data:
                services = raw_data["services"]
            elif "produits" in raw_data:
                services = raw_data["produits"]
            elif "items" in raw_data:
                services = raw_data["items"]
                
            # Extraire le montant total
            montant_total = raw_data.get("montant_total", 0.0)
            
            # Extraire la TVA
            tva = raw_data.get("tva", 20.0)
            
            return FactureData(
                numero_facture=numero_facture,
                date=date,
                client_nom=client_nom,
                client_adresse=client_adresse,
                services=services,
                montant_total=montant_total,
                tva=tva
            )
            
        except Exception as e:
            print(f"Erreur lors de la génération de la structure facture: {e}")
            # Retourner une structure minimale
            return FactureData(
                numero_facture="FACT-001",
                date=datetime.now(),
                client_nom="Client non spécifié"
            )
    
    def _generate_report_structure(self, raw_data: Dict[str, Any]) -> RapportData:
        """Génère la structure pour un rapport"""
        try:
            # Extraire les informations de base
            titre = raw_data.get("titre", "Titre non spécifié")
            auteur = raw_data.get("auteur", "Auteur non spécifié")
            
            # Extraire la date
            date_str = raw_data.get("date")
            if date_str:
                try:
                    date = datetime.fromisoformat(date_str)
                except:
                    date = datetime.now()
            else:
                date = datetime.now()
                
            # Extraire le résumé
            resume = raw_data.get("resume")
            
            # Extraire les sections
            sections = []
            if "sections" in raw_data:
                sections = raw_data["sections"]
            elif "chapitres" in raw_data:
                sections = raw_data["chapitres"]
            elif "contenu" in raw_data:
                # Si c'est un texte simple, créer une section unique
                sections = [{"titre": "Contenu", "contenu": raw_data["contenu"]}]
                
            # Extraire les conclusions
            conclusions = raw_data.get("conclusions")
            
            return RapportData(
                titre=titre,
                auteur=auteur,
                date=date,
                resume=resume,
                sections=sections,
                conclusions=conclusions
            )
            
        except Exception as e:
            print(f"Erreur lors de la génération de la structure rapport: {e}")
            # Retourner une structure minimale
            return RapportData(
                titre="Titre non spécifié",
                auteur="Auteur non spécifié",
                date=datetime.now()
            )