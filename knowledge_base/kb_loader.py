from pathlib import Path


KB_FILE = Path(__file__).parent / "languages.md"

documents = {}


def load_docs():
    if KB_FILE.exists():
        documents["languages"] = KB_FILE.read_text(encoding="utf-8")
        print("Loaded knowledge base: languages.md")


def search(query: str) -> str:
    if not documents:
        return ""

    query_words = query.lower().split()

    # Score each document by keyword frequency
    scores = {}
    for name, content in documents.items():
        content_lower = content.lower()
        score = sum(content_lower.count(word) for word in query_words if len(word) > 2)
        if score > 0:
            scores[name] = score

    if not scores:
        return ""

    # Return top 2 matches joined as context
    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2]
    return "\n\n---\n\n".join(documents[name] for name, _ in top)


load_docs()