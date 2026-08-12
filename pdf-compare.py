import sys
import difflib
from pathlib import Path

from pypdf import PdfReader


# ============================================================
# FR: Extraction du texte
# EN: Text extraction
# ============================================================

def extract_text(pdf_path):
    """
    FR: Extrait le texte de toutes les pages d'un fichier PDF.
    EN: Extracts text from all pages of a PDF file.
    """

    reader = PdfReader(pdf_path)
    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


# ============================================================
# FR: Normalisation du texte
# EN: Text normalization
# ============================================================

def normalize_text(text):
    """
    FR: Nettoie les lignes avant comparaison.
    EN: Cleans lines before comparison.
    """

    lines = []

    for line in text.splitlines():
        clean_line = " ".join(line.split())

        if clean_line:
            lines.append(clean_line)

    return lines


# ============================================================
# FR: Comparaison des PDF
# EN: PDF comparison
# ============================================================

def compare_pdfs(old_pdf, new_pdf):
    """
    FR: Compare le contenu textuel de deux fichiers PDF.
    EN: Compares the textual content of two PDF files.
    """

    old_text = extract_text(old_pdf)
    new_text = extract_text(new_pdf)

    old_lines = normalize_text(old_text)
    new_lines = normalize_text(new_text)

    differences = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=Path(old_pdf).name,
            tofile=Path(new_pdf).name,
            lineterm=""
        )
    )

    return differences


# ============================================================
# FR: Affichage du résultat
# EN: Result display
# ============================================================

def display_result(differences):
    """
    FR: Affiche les différences détectées.
    EN: Displays detected differences.
    """

    if not differences:
        print("FR: Aucune différence détectée.")
        print("EN: No differences detected.")
        return

    print("\n===== PDF COMPARISON =====\n")

    for line in differences:
        print(line)


# ============================================================
# FR: Point d'entrée
# EN: Entry point
# ============================================================

def main():
    """
    FR: Attend deux chemins de fichiers PDF en arguments.
    EN: Expects two PDF file paths as arguments.
    """

    if len(sys.argv) != 3:
        print("FR: Utilisation : python pdf_compare.py ancien.pdf nouveau.pdf")
        print("EN: Usage: python pdf_compare.py old.pdf new.pdf")
        sys.exit(1)

    old_pdf = Path(sys.argv[1])
    new_pdf = Path(sys.argv[2])

    if not old_pdf.is_file():
        print(f"FR: Fichier introuvable : {old_pdf}")
        print(f"EN: File not found: {old_pdf}")
        sys.exit(1)

    if not new_pdf.is_file():
        print(f"FR: Fichier introuvable : {new_pdf}")
        print(f"EN: File not found: {new_pdf}")
        sys.exit(1)

    if old_pdf.suffix.lower() != ".pdf" or new_pdf.suffix.lower() != ".pdf":
        print("FR: Les deux fichiers doivent être au format PDF.")
        print("EN: Both files must be PDF files.")
        sys.exit(1)

    try:
        differences = compare_pdfs(old_pdf, new_pdf)
        display_result(differences)

    except Exception as error:
        print(f"FR: Erreur pendant la comparaison : {error}")
        print(f"EN: Error during comparison: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
