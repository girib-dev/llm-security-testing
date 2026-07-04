import anthropic
import re

client = anthropic.Anthropic()

BLOCKED_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"system prompt",
    r"you are now",
    r"do anything now",
    r"internal configuration",
]

def is_suspicious(user_input):
    return any(re.search(p, user_input, re.IGNORECASE) for p in BLOCKED_PATTERNS)

def ask_assistant(user_input):
    if is_suspicious(user_input):
        return "[BLOCKED: This input matched a known prompt injection pattern.]"

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        system="You are a helpful customer support assistant for a fictional company called Acme Corp. Only answer questions about Acme's products.",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.content[0].text

if __name__ == "__main__":
    print(ask_assistant("What are Acme Corp's return policies?"))
