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
        """Génère la structure pour un CV de manière robuste"""
        try:
            def _extract_list(raw_data: dict, possible_keys: list) -> list:
                """Retourne la première liste trouvée parmi les clés possibles"""
                for key in possible_keys:
                    if key in raw_data and isinstance(raw_data[key], list):
                        return [item for item in raw_data[key] if item]
                return []

            # Informations de base
            nom = raw_data.get("nom", "Nom non spécifié")
            email = raw_data.get("email")
            telephone = raw_data.get("telephone") or raw_data.get("téléphone")
            adresse = raw_data.get("adresse")

            # Poste éventuel
            poste = raw_data.get("poste") or raw_data.get("position")

            # Listes extraites
            experiences = _extract_list(
                raw_data,
                ["experiences", "experience", "experiences_professionnelles", "expériences", "expérience"]
            )
            formations = _extract_list(
                raw_data,
                ["formations", "formation", "formations_academiques"]
            )
            competences = _extract_list(
                raw_data,
                ["competences", "competence", "skills", "compétences", "compétence"]
            )

            # 🔹 Transformer dicts en texte pour le PDF
            experiences = [
                f"{e.get('poste', '')} chez {e.get('entreprise', '')} ({e.get('période', '')})"
                if isinstance(e, dict) else str(e)
                for e in experiences
            ]
            formations = [
                f"{f.get('diplôme', '')}, {f.get('lieu', f.get('établissement', ''))} ({f.get('année', '')})"
                if isinstance(f, dict) else str(f)
                for f in formations
            ]
            competences = [str(c) for c in competences if str(c).strip()]

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
            return CVData(nom="Nom non spécifié")


    
    def _generate_invoice_structure(self, raw_data: Dict[str, Any]) -> FactureData:
        """Génère la structure pour une facture"""
        try:
            numero_facture = raw_data.get("numero_facture") or raw_data.get("numéro") or "FACT-001"
            date_str = raw_data.get("date")
            if date_str:
                try:
                    date = datetime.fromisoformat(date_str)
                except:
                    try:
                        date = datetime.strptime(date_str, "%d/%m/%Y")
                    except:
                        date = datetime.now()
            else:
                date = datetime.now()

            client_nom = raw_data.get("client_nom") or raw_data.get("client") or "Client non spécifié"
            client_adresse = raw_data.get("client_adresse") or raw_data.get("adresse")
            fournisseur = raw_data.get("fournisseur")
            email_fournisseur = raw_data.get("email_fournisseur")
            date_emission = raw_data.get("date_emission")
            date_echeance = raw_data.get("date_echeance")

            services = raw_data.get("services") or raw_data.get("produits") or raw_data.get("items") or []
            # Si services est une chaîne, essayer de parser en liste
            if isinstance(services, str):
                services = [services]

            montant_total = raw_data.get("montant_total", 0.0)
            # Si montant_total absent, le calculer à partir des services
            if not montant_total and services:
                montant_total = sum(
                    s.get("quantite", 1) * s.get("prix_unitaire", 0.0)
                    for s in services if isinstance(s, dict)
                )

            tva = raw_data.get("tva", 20.0)
            total_ttc = raw_data.get("total_ttc")
            conditions = raw_data.get("conditions")
            mentions_legales = raw_data.get("mentions_legales")
            remarques = raw_data.get("remarques")

            # Adapter ici selon la définition de FactureData (ajouter les champs si besoin)
            return FactureData(
                numero_facture=numero_facture,
                date=date,
                client_nom=client_nom,
                client_adresse=client_adresse,
                services=services,
                montant_total=montant_total,
                tva=tva,
                fournisseur=fournisseur,
                email_fournisseur=email_fournisseur,
                date_emission=date_emission,
                date_echeance=date_echeance,
                total_ttc=total_ttc,
                conditions=conditions,
                mentions_legales=mentions_legales,
                remarques=remarques
            )
        except Exception as e:
            print(f"Erreur lors de la génération de la structure facture: {e}")
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