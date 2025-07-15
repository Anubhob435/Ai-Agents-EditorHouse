"""
    Agent responsible for enhancing the formatting of generated book content.
    Applies styling like bold and italics, cleans up unnecessary content,
    and improves the overall presentation of the markdown.
"""

from .agent import editor_agent

__all__ = ["editor_agent"]