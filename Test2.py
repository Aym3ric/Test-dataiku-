# Exemple de structure d'artefact renvoyée par le Code Agent
artifact = {
    "id": "word-report-1",
    "type": "FILE",              # Indique à l'UI DSS qu'il s'agit d'un fichier téléchargeable
    "name": "Rapport_Synthese.docx",
    "description": "Document Word généré par l'agent",
    "parts": [
        {
            "type": "BINARY",
            "index": 0,
            # Le contenu binaire encodé en base64 ou la référence interne de stockage
            "data": encoded_docx_base64
        }
    ]
}

# Dans le retour de complétion de ton agent :
return {
    "ok": True,
    "text": "Voici le document généré sous forme d'artefact :",
    "finishReason": "STOP",
    "artifacts": [artifact]
}
