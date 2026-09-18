import dataiku
from dataiku.llm.python import BaseLLM
import base64
import io
from docx import Document
import pandas as pd

OPENAI_CONNECTION_NAME = "openai:LLMaaS-Qwen3-32B:/model/Qwen3-32B-FP8"

class DirectFileArtifactAgent(BaseLLM):
    def __init__(self):
        pass

    def process(self, query, settings, trace):
        prompt = query["messages"][-1]["content"]
        
        # Déterminer le type de document à créer
        if any(word in prompt.lower() for word in ["word", "docx", "document"]):
            artifacts = [self._create_word_artifact(prompt)]
            response_text = "J'ai créé un document Word que vous pouvez télécharger."
        else:
            artifacts = [self._create_word_artifact(prompt)]
            response_text = "J'ai créé un document Word basé sur votre demande."
        
        return {
            "ok": True,
            "text": "Voici le document généré sous forme d'artefact :",
            "finishReason": "STOP",
            "artifacts": artifacts
        }

    def _create_word_artifact(self, topic):
        """Crée un artefact Word avec la structure Dataiku"""
        
        # Créer le document Word
        doc = Document()
        doc.add_heading(f'Document : {topic}', 0)
        doc.add_paragraph(f'Ce document a été généré automatiquement sur le sujet : {topic}')
        doc.add_heading('Contenu Principal', level=1)
        doc.add_paragraph('Voici le contenu détaillé du document.')
        
        # Convertir en bytes
        doc_buffer = io.BytesIO()
        doc.save(doc_buffer)
        doc_buffer.seek(0)
        doc_bytes = doc_buffer.getvalue()
        doc_base64 = base64.b64encode(doc_bytes).decode('utf-8')
        
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
                    "data": doc_base64
                }
            ]
        }
        return artifact
    
