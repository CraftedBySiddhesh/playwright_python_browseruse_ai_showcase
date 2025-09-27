from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from langchain_core.messages import HumanMessage

from utils.logger import configure_logger, redact_secrets
from utils.settings import Settings, load_settings

logger = configure_logger("ai_providers")


class ProviderProtocol(Protocol):
    def generate(self, prompt: str) -> str: ...


@dataclass
class StubProvider:
    seed: int = 42

    def generate(self, prompt: str) -> str:
        deterministic_responses = {
            "checkout": "Order completed successfully.",
            "login": "Login completed with provided credentials.",
            "error": "Encountered expected validation error.",
        }
        for key, message in deterministic_responses.items():
            if key in prompt.lower():
                return message
        return "Action completed using stub provider."


@dataclass
class LiveProvider:
    model_name: str
    api_key: str
    provider: str

    def _client(self):
        if self.provider == "groq":
            from langchain_groq import ChatGroq

            return ChatGroq(groq_api_key=self.api_key, model_name=self.model_name)
        if self.provider == "openai":
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(api_key=self.api_key, model=self.model_name)
        raise ValueError(f"Unsupported provider: {self.provider}")

    def generate(self, prompt: str) -> str:
        client = self._client()
        logger.info("Invoking live provider", extra=redact_secrets({"provider": self.provider}))
        response = client.invoke([HumanMessage(content=prompt)])
        return response.content or ""


@dataclass
class ProviderFactory:
    settings: Settings

    def build(self) -> ProviderProtocol:
        if not self.settings.use_live_provider:
            return StubProvider(seed=self.settings.app.seed)

        if self.settings.llm_provider == "groq" and self.settings.groq_api_key:
            return LiveProvider(
                model_name="llama-3.3-70b-versatile",
                api_key=self.settings.groq_api_key,
                provider="groq",
            )
        if self.settings.llm_provider == "openai" and self.settings.openai_api_key:
            return LiveProvider(
                model_name="gpt-4o-mini", api_key=self.settings.openai_api_key, provider="openai"
            )
        logger.warning("Falling back to stub provider due to missing credentials")
        return StubProvider(seed=self.settings.app.seed)


def get_provider(settings: Settings | None = None) -> ProviderProtocol:
    if settings is None:
        settings = load_settings()
    factory = ProviderFactory(settings=settings)
    return factory.build()
