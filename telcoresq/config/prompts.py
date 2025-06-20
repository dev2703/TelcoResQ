# Prompts for TelcoResQ

# Example prompt for theme extraction
THEME_EXTRACTION_PROMPT = """
Analyze the following survey responses about telecom network resilience and identify the main themes.
For each theme, provide a brief description and a representative quote from the responses.

Survey responses:
---
{responses}
---

Themes:
"""

# Example prompt for sentiment analysis
SENTIMENT_ANALYSIS_PROMPT = """
Classify the sentiment of the following survey response as positive, negative, or neutral.
Provide a one-sentence justification for your classification.

Survey response:
---
{response}
---

Sentiment:
Justification:
"""

# Example prompt for summary generation
SUMMARY_GENERATION_PROMPT = """
Summarize the key insights from the following survey responses regarding telecom network resilience.
The summary should be about 100 words and highlight the most critical issues and suggestions.

Survey responses:
---
{responses}
---

Summary:
"""
