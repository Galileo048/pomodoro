"""DeepSeek API client for AI-assisted animation generation."""

from __future__ import annotations

import json
import logging
from typing import Any

from openai import APIError, APIConnectionError, OpenAI

from formula2manim.ai_assistant.prompts import (
    CODE_MODIFICATION,
    ERROR_DIAGNOSIS,
    MODEL_SUGGESTION,
    NATURAL_LANGUAGE_TO_FORMULA,
    SCENE_ENHANCEMENT,
)
from formula2manim.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEFAULT_AI_MODEL,
)
from formula2manim.exceptions import DeepSeekAPIError

logger = logging.getLogger(__name__)


class DeepSeekClient:
    """Client for the DeepSeek API (OpenAI-compatible).

    API key resolution (priority order):
    1. Constructor parameter api_key
    2. DEEPSEEK_API_KEY environment variable
    3. .env file (loaded by python-dotenv in config.py)
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_AI_MODEL,
        base_url: str = DEEPSEEK_BASE_URL,
    ) -> None:
        resolved_key = api_key or DEEPSEEK_API_KEY
        if not resolved_key:
            raise DeepSeekAPIError(
                "DeepSeek API key not found. Provide it via:\n"
                "  1. --api-key CLI argument\n"
                "  2. DEEPSEEK_API_KEY environment variable\n"
                "  3. .env file with DEEPSEEK_API_KEY=sk-..."
            )
        self.model = model
        self.client = OpenAI(api_key=resolved_key, base_url=base_url)

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> str:
        """Send a chat completion request and return the response text."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore[arg-type]
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content
            return content.strip() if content else ""
        except APIConnectionError as e:
            raise DeepSeekAPIError(
                f"Cannot connect to DeepSeek API at {DEEPSEEK_BASE_URL}. "
                f"Check your network or base URL.\nDetails: {e}"
            ) from e
        except APIError as e:
            raise DeepSeekAPIError(
                f"DeepSeek API error: {e}\n"
                "Check your API key and account status."
            ) from e

    def _parse_json_response(self, response: str) -> dict[str, Any]:
        """Parse JSON from AI response, with retry logic for malformed output."""
        # Strip potential markdown fences
        cleaned = response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            # Remove opening fence
            if lines[0].startswith("```"):
                lines = lines[1:]
            # Remove closing fence
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines)

        try:
            return json.loads(cleaned)  # type: ignore[no-any-return]
        except json.JSONDecodeError:
            # Try extracting JSON from within the response
            import re
            match = re.search(r"\{[^{}]*\{[^{}]*\}[^{}]*\}|\{[^{}]*\}", cleaned)
            if match:
                try:
                    return json.loads(match.group())  # type: ignore[no-any-return]
                except json.JSONDecodeError:
                    pass
            raise DeepSeekAPIError(
                "AI returned non-JSON output. Try again or provide formulas "
                "directly with --formulas.\n"
                f"Raw response:\n{response[:500]}"
            )

    def generate_formula(self, description: str) -> dict[str, Any]:
        """Convert a natural language description into a formula + params.

        Args:
            description: e.g. "A ball thrown at 10 m/s horizontally from 20m."

        Returns:
            Dict with keys: formulas, params, explanation, suggested_t_range.
        """
        messages = [
            {"role": "system", "content": NATURAL_LANGUAGE_TO_FORMULA},
            {"role": "user", "content": description},
        ]
        response = self.chat(messages)
        return self._parse_json_response(response)

    def suggest_model(
        self, formulas: dict[str, Any], params: dict[str, float | str | list | dict]
    ) -> dict[str, Any]:
        """Suggest which physics model fits the given formulas and params."""
        # Send parameter values (truncated) so AI can see types like JSON arrays
        param_info = {}
        for k, v in params.items():
            s = str(v)
            param_info[k] = s[:100] + "..." if len(s) > 100 else s

        info = {
            "variables": list(formulas.keys()),
            "parameters": param_info,
            "formula_strings": {k: str(v) for k, v in formulas.items()},
        }
        messages = [
            {"role": "system", "content": MODEL_SUGGESTION},
            {"role": "user", "content": json.dumps(info, indent=2)},
        ]
        response = self.chat(messages)
        return self._parse_json_response(response)

    def enhance_scene(self, model_info: dict[str, Any]) -> dict[str, Any]:
        """Suggest visual enhancements for the Manim scene."""
        messages = [
            {"role": "system", "content": SCENE_ENHANCEMENT},
            {"role": "user", "content": json.dumps(model_info, indent=2)},
        ]
        response = self.chat(messages)
        return self._parse_json_response(response)

    def modify_code(self, current_code: str, request: str) -> str:
        """Modify Manim source code based on a natural language request.

        Args:
            current_code: The current Manim Python source code.
            request: User's modification request (Chinese or English).

        Returns:
            The modified Python source code.
        """
        messages = [
            {"role": "system", "content": CODE_MODIFICATION},
            {"role": "user", "content": (
                f"Current code:\n```python\n{current_code}\n```\n\n"
                f"Modification request: {request}\n\n"
                f"Output the complete modified code (no markdown, no explanation):"
            )},
        ]
        response = self.chat(messages, temperature=0.2, max_tokens=4096)
        return self._strip_code_fences(response)

    def _strip_code_fences(self, text: str) -> str:
        """Remove markdown code fences from AI response."""
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            return "\n".join(lines)
        return text

    def diagnose_error(
        self, error_output: str, formulas: str, params: str
    ) -> dict[str, Any]:
        """Diagnose a Manim rendering error and suggest a fix."""
        prompt = ERROR_DIAGNOSIS.format(
            error_output=error_output[-3000:],
            formulas=formulas,
            params=params,
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Please diagnose this error."},
        ]
        response = self.chat(messages)
        return self._parse_json_response(response)
