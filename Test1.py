import io
import base64
from typing import Any, List, Optional
import docx

from langchain_core.language_models.llms import BaseLLM
from langchain_core.outputs import LLMResult, Generation
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

def create_docx_base64(title: str, body: str) -> str:
    """Génère le binaire Word en mémoire et le convertit en Base64."""
    doc = docx.Document()
    doc.add_heading(title, level=1)
    
    for paragraph in body.split("\n\n"):
        p = paragraph.strip()
        if p:
            doc.add_paragraph(p)
            
    buffer = io.BytesIO()
    doc.save(buffer)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


class MyLLM(BaseLLM):
    """
    Code Agent Dataiku 14.3+ émettant un artefact Word natif.
    """

    @property
    def _llm_type(self) -> str:
        return "dataiku_custom_agent"

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        generations = []

        for prompt in prompts:
            # 1. Génération du document Word en base64
            doc_name = "Rapport_Analyse.docx"
            b64_content = create_docx_base64(
                title="Rapport de Synthèse",
                body=(
                    f"Requête initiale de l'utilisateur :\n{prompt}\n\n"
                    "Ce document a été produit dynamiquement sous forme d'artefact."
                )
            )

            # 2. Spécification officielle de l'artefact Dataiku DSS 14.3
            artifact = {
                "id": "word-report-artifact",
                "type": "FILE",
                "name": doc_name,
                "description": "Document Word généré par le Code Agent",
                "parts": [
                    {
                        "type": "DATA_INLINE",
                        "index": 0,
                        "mimeType": DOCX_MIME,
                        "dataBase64": b64_content
                    }
                ]
            }

            # 3. Message texte retourné dans le chat
            chat_text = "Voici votre document Word généré sous forme d'artefact."

            # 4. Transmission à Dataiku via le generation_info
            gen = Generation(
                text=chat_text,
                generation_info={
                    "artifacts": [artifact],
                    "finish_reason": "STOP"
                }
            )
            generations.append([gen])

        return LLMResult(generations=generations)
