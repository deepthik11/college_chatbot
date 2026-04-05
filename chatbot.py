from groq import Groq
import requests
from bs4 import BeautifulSoup

# 🔑 ADD YOUR API KEY HERE
client = Groq(api_key="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")

# College URLs
urls = [
    "https://vcetputtur.ac.in/",
    "https://vcetputtur.ac.in/about-vcet/",
    "https://vcetputtur.ac.in/academics/",
    "https://vcetputtur.ac.in/placements/",
    "https://vcetputtur.ac.in/contact-us/"
]

# Fetch website text
def get_website_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style"]):
            script.extract()

        return soup.get_text(separator=" ", strip=True)

    except Exception as e:
        print(f"Error loading {url}: {e}")
        return ""

# Load all data ONCE
all_text = ""
for url in urls:
    print(f"Loading: {url}")
    all_text += get_website_text(url) + "\n"

# Split text into chunks
def split_text(text, chunk_size=800):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

chunks = split_text(all_text)

# Find relevant chunks
def find_relevant_chunks(question, chunks):
    question_words = question.lower().split()
    scored = []

    for chunk in chunks:
        score = sum(word in chunk.lower() for word in question_words)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(reverse=True)
    return [c for _, c in scored[:3]]

# MAIN FUNCTION (used by frontend)
def ask_bot(question):

    relevant_chunks = find_relevant_chunks(question, chunks)

    if not relevant_chunks:
        return "Information not available on website."

    context = "\n".join(relevant_chunks)

    prompt = f"""
Answer ONLY from the context below.
If answer not found, say: Information not available on website.

Context:
{context}

Question: {question}
Answer:
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {e}"
