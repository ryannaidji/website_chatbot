"""
LLM Interface Module

Handles interaction with local LLM (Ollama).
"""

import requests
from typing import Optional


class LLMInterface:
    """Interface for local LLM using Ollama."""

    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        """
        Initialize LLM interface.

        Args:
            model: Ollama model name to use
            base_url: Base URL for Ollama API
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"

    def is_available(self) -> bool:
        """
        Check if Ollama is running and accessible.

        Returns:
            True if Ollama is available
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def generate_response(self, question: str, context: str) -> str:
        """
        Generate a response using the LLM with provided context.

        Args:
            question: User's question
            context: Relevant context from vector store

        Returns:
            Generated response
        """
        # Build prompt with context
        prompt = self._build_prompt(question, context)

        try:
            # Call Ollama API
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 500
                    }
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response generated.')
            else:
                return f"Error: LLM returned status {response.status_code}"

        except Exception as e:
            return f"Error communicating with LLM: {e}"

    def _build_prompt(self, question: str, context: str) -> str:
        """
        Build a prompt with context for the LLM.

        Args:
            question: User's question
            context: Retrieved context

        Returns:
            Formatted prompt
        """
        prompt = f"""You are a helpful assistant that answers questions based on website content.

Context from the website:
{context}

Question: {question}

Answer the question based on the context provided above. If the context doesn't contain relevant information, say so. Be concise and helpful.

Answer:"""

        return prompt
