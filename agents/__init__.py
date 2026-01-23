"""
Multi-Agent Content Generation System using CrewAI.

Agents:
- Director: Routes content requests to specialized agents
- BlogAgent: Long-form blog posts
- LinkedInAgent: Professional LinkedIn posts
- TwitterAgent: Concise tweets and threads
- InstagramAgent: Visual captions with hashtags
- Revisor: Content validation and quality control
"""

from .content_crew import ContentCrew

__all__ = ["ContentCrew"]
