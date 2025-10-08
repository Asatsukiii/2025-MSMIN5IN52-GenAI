"""
Démonstration interactive du générateur de contenu structuré
Permet de choisir entre des exemples prédéfinis ou d'entrer du texte manuellement
"""
import os
import sys
from src.orchestrator import DocumentOrchestrator, generate_document_from_text
from datetime import datetime

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def clear_screen():
    """Efface l'écran de la console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Affiche l'en-tête du programme"""
    clear_screen()
    print("=" * 60)
    print("    🚀 GÉNÉRATEUR DE CONTENU STRUCTURÉ - MODE INTERACTIF")
    print("=" * 60)
    print()

def print_menu():
    """Affiche le menu principal"""
    print("📋 CHOISISSEZ UNE OPTION:")
    print()
    print("1. 📄 Générer un CV simple")
    print("2. 📄 Générer un CV complexe")
    print("3. 🧾 Générer une facture simple")
    print("4. 🧾 Générer une facture détaillée")
    print("5. 📊 Générer un rapport simple")
    print("6. ✍️  Entrer du texte manuellement")
    print("7. ❌ Quitter")
    print()

def get_user_text():
    """Obtenir du texte de l'utilisateur"""
    print("\n📝 Entrez votre texte (terminez par une ligne vide):")
    print("💡 Exemples: description de CV, détails de facture, contenu de rapport")
    print()
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break
    
    return "\n".join(lines)

async def process_manual_input():
    """Traiter une entrée manuelle"""
    text = get_user_text()
    if not text.strip():
        print("❌ Aucun texte saisi.")
        return
    
    print("\n🔍 Analyse en cours...")
    orchestrator = DocumentOrchestrator()
    
    try:
        # Analyser le texte
        extracted_data = await orchestrator.text_analyzer.analyze_text(text)
        document_type = extracted_data.document_type
        confidence = extracted_data.confidence_score
        print(f"✅ Type détecté: {document_type.upper()} (confiance: {confidence:.0%})")
        
        # Générer le PDF
        output_path = f"projet 14 GOFFINET-EL MOKHTARI-BERRICHI/output/manual_{document_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = await generate_document_from_text(text, output_path)
        
        if pdf_path:
            print(f"🎉 Document généré avec succès: {pdf_path}")
        else:
            print("❌ Échec de la génération du document")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Fonction principale"""
    while True:
        print_header()
        print_menu()
        
        try:
            choice = input("👉 Votre choix (1-7): ").strip()
            
            if choice == '7':
                print("\n👋 Au revoir !")
                break
                
            if choice == '1':
                from test_examples import test_cv_simple
                print("\n🚀 Génération du CV simple...")
                import asyncio
                asyncio.run(test_cv_simple())
                print("✅ CV simple généré: output/test_cv_simple.pdf")
                
            elif choice == '2':
                from test_examples import test_cv_complexe
                print("\n🚀 Génération du CV complexe...")
                import asyncio
                asyncio.run(test_cv_complexe())
                print("✅ CV complexe généré: output/test_cv_complexe.pdf")
                
            elif choice == '3':
                from test_examples import test_facture_simple
                print("\n🚀 Génération de la facture simple...")
                import asyncio
                asyncio.run(test_facture_simple())
                print("✅ Facture simple générée: output/test_facture_simple.pdf")
                
            elif choice == '4':
                from test_examples import test_facture_detaillée
                print("\n🚀 Génération de la facture détaillée...")
                import asyncio
                asyncio.run(test_facture_detaillée())
                print("✅ Facture détaillée générée: output/test_facture_detaillée.pdf")
                
            elif choice == '5':
                from test_examples import test_rapport_simple
                print("\n🚀 Génération du rapport simple...")
                import asyncio
                asyncio.run(test_rapport_simple())
                print("✅ Rapport simple généré: output/test_rapport_simple.pdf")
                
            elif choice == '6':
                import asyncio
                asyncio.run(process_manual_input())
                
            else:
                print("\n❌ Choix invalide. Veuillez choisir entre 1 et 7.")
            
            print("\n" + "-" * 60)
            input("👉 Appuyez sur Entrée pour continuer...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            input("👉 Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()