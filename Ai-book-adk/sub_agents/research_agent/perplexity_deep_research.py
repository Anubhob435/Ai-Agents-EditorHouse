import os
from openai import OpenAI
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.getenv("SONAR_API_KEY")
if not API_KEY:
    raise RuntimeError("SONAR_API_KEY not set. Add it to your environment or .env file.")

# Initialize OpenAI client for Perplexity
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.perplexity.ai"
)


def perplexity_deep_research(query=None):
    """
    Conduct deep research using Perplexity's sonar-deep-research model.
    
    Args:
        query (str, optional): Research query. If None, uses default quantum computing query.
    
    Returns:
        str: The research response content
    """

    if query is None:
        query = "Conduct a comprehensive analysis of the quantum computing industry, including technological approaches, key players, market opportunities, regulatory challenges, and commercial viability projections through 2035."
    
    response = client.chat.completions.create(
        model="sonar-deep-research",
        messages=[
            {"role": "user", "content": query}
        ],
        max_tokens=2048,  # Deep research typically needs more tokens
        temperature=0.1,  # Lower temperature for factual research
        stream=False
    )
    
    content = response.choices[0].message.content
    
    # Print the response
    print("\n--- Perplexity Deep Research Response ---\n")
    print(content)
    
    # Print citations if available
    citations = getattr(response, 'citations', None)
    if citations:
        print("\nCitations:")
        for i, url in enumerate(citations, 1):
            print(f"  {i}. {url}")
    
    # Save response to markdown file
    md_filename = "deep_research_answer.md"
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write("# Perplexity Deep Research Analysis\n\n")
        f.write(f"**Query:** {query}\n\n")
        f.write("## Research Results\n\n")
        f.write(content + "\n\n")
        if citations:
            f.write("## Citations\n\n")
            for i, url in enumerate(citations, 1):
                f.write(f"{i}. {url}\n")
    
    print(f"\nResponse saved to {md_filename}")
    
    return content

# Example usage:
result = perplexity_deep_research()
custom_result = perplexity_deep_research("Analyze the latest developments in AI safety research")
