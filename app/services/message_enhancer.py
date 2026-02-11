from app.services.llm_factory import get_llm
import os

llm = get_llm()
provider = os.getenv("LLM_PROVIDER", "azure")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
model_name = os.getenv("GEMINI_MODEL")


def enhance_message(raw_message: str) -> str:
    """
    Converts backend/system messages into friendly user-facing text.
    """

    system_prompt = (
        "You are a helpful enterprise assistant. "
        "Rewrite the given system message into a friendly, clear, "
        "user-facing response. Be polite and reassuring. "
        "Do NOT mention technical details."
    )

    # Azure
    if provider == "azure":
        response = llm.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_message}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()

    # Gemini
    else:
        prompt = f"""
{system_prompt}

Message:
{raw_message}
""".strip()

        response = llm.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text.strip()