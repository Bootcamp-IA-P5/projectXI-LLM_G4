"""
Content Generation Crew with CrewAI.
Orchestrates multiple specialized agents for content creation.
"""
import os
import re
from typing import Dict, Any

# Disable CrewAI telemetry to avoid signal handler issues in Streamlit
os.environ["OTEL_SDK_DISABLED"] = "true"
# Disable CrewAI tracing
os.environ["CREWAI_TRACING_ENABLED"] = "false"

from crewai import Agent, Task, Crew, Process, LLM

from .tools.guardrails import validate_content, check_tone_consistency


class ContentCrew:
    """
    Multi-agent content generation system using CrewAI.
    
    Agents:
    - Director: Routes requests to specialized agents
    - Content Agents: Blog, LinkedIn, Twitter, Instagram
    - Revisor: Validates content quality
    """
    
    def __init__(self, provider: str = "groq", model: str = "llama-3.1-8b-instant"):
        """
        Initialize the content crew.
        Args:
            provider: LLM provider (groq, ollama)
            model: Model name
        """
        self.provider = provider
        self.model = model
        self.llm = self._get_llm()
        
    def _get_llm(self):
        """Get configured LLM instance using CrewAI's native LLM class."""
        if self.provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment")
            # Use CrewAI's native LLM format for Groq
            return LLM(
                model=f"groq/{self.model}",
                api_key=api_key,
                temperature=0.7
            )
        
        elif self.provider == "ollama":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            # Use CrewAI's native LLM format for Ollama
            return LLM(
                model=f"ollama/{self.model}",
                base_url=base_url,
                temperature=0.7
            )
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}. Use 'groq' or 'ollama'")
    
    def _create_director_agent(self) -> Agent:
        """Create the director agent that routes requests."""
        return Agent(
            role="Content Director",
            goal="Analyze content requests and route them to the appropriate specialized agent",
            backstory="""You are an expert content strategist with deep knowledge of digital 
            marketing across all platforms. You understand the unique requirements of each 
            platform and can determine which specialist is best suited for each request.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
    
    def _create_blog_agent(self) -> Agent:
        """Create the blog content specialist agent."""
        return Agent(
            role="Blog Content Specialist",
            goal="Create engaging, SEO-optimized long-form blog posts",
            backstory="""You are a professional blog writer with expertise in creating 
            comprehensive, well-structured articles. You excel at storytelling, maintaining 
            reader engagement, and optimizing content for search engines. Your posts have 
            clear introductions, detailed bodies, and compelling conclusions.""",
            verbose=True,
            llm=self.llm
        )
    
    def _create_linkedin_agent(self) -> Agent:
        """Create the LinkedIn content specialist agent."""
        return Agent(
            role="LinkedIn Content Specialist",
            goal="Create professional and engaging LinkedIn posts",
            backstory="""You are a LinkedIn content expert who understands professional 
            networking. You craft posts that balance professionalism with personality, 
            using compelling hooks, valuable insights, and clear calls-to-action. You know 
            how to engage B2B audiences and build thought leadership.""",
            verbose=True,
            llm=self.llm
        )
    
    def _create_twitter_agent(self) -> Agent:
        """Create the Twitter/X content specialist agent."""
        return Agent(
            role="Twitter Content Specialist",
            goal="Create concise, impactful tweets and threads",
            backstory="""You are a social media expert specializing in Twitter/X. You master 
            the art of brevity, creating punchy tweets that grab attention and spark 
            engagement. You know how to craft viral threads, use hashtags effectively, 
            and create content that resonates with diverse audiences.""",
            verbose=True,
            llm=self.llm
        )
    
    def _create_instagram_agent(self) -> Agent:
        """Create the Instagram content specialist agent."""
        return Agent(
            role="Instagram Content Specialist",
            goal="Create captivating Instagram captions with strong visual appeal",
            backstory="""You are an Instagram content creator who understands visual 
            storytelling. You write captions that complement images perfectly, using 
            emojis strategically, crafting engaging hooks, and leveraging hashtags for 
            maximum reach. You know how to build community and drive engagement.""",
            verbose=True,
            llm=self.llm
        )
    
    def _create_revisor_agent(self) -> Agent:
        """Create the content reviewer agent."""
        return Agent(
            role="Content Quality Reviewer",
            goal="Validate content quality, detect issues, and ensure compliance with guidelines",
            backstory="""You are a meticulous content quality assurance specialist. You 
            review content for accuracy, tone consistency, appropriate length, and 
            potential issues like hallucinations or inappropriate language. You ensure 
            all content meets professional standards before publication.""",
            verbose=True,
            llm=self.llm
        )
    
    def generate_content(
        self,
        platform: str,
        topic: str,
        audience: str,
        tone: str = "professional",
        language: str = "English",
        user_profile: Dict[str, str] = None,
        include_images: bool = False
    ) -> Dict[str, Any]:
        """
        Generate content using the multi-agent crew.
        
        Args:
            platform: Target platform (Blog, LinkedIn, Twitter, Instagram)
            topic: Content topic
            audience: Target audience
            tone: Content tone (professional, friendly, bold)
            language: Output language
            user_profile: Optional user/brand profile information
            include_images: Whether to generate images
        
        Returns:
            Dictionary with generated content and metadata
        """
        # Create agents
        director = self._create_director_agent()
        revisor = self._create_revisor_agent()
        
        # Select appropriate content agent
        agent_map = {
            "Blog": self._create_blog_agent(),
            "LinkedIn": self._create_linkedin_agent(),
            "Twitter": self._create_twitter_agent(),
            "Instagram": self._create_instagram_agent()
        }
        
        # Clean platform name
        platform_clean = platform.replace("📝 ", "").replace("💼 ", "").replace("🐦 ", "").replace("📸 ", "")
        content_agent = agent_map.get(platform_clean)
        
        if not content_agent:
            raise ValueError(f"Unsupported platform: {platform}")
        
        # Build context with user profile
        profile_context = ""
        if user_profile and any(user_profile.values()):
            profile_context = f"""
            
Brand/User Profile:
- Name: {user_profile.get('name', 'N/A')}
- Industry: {user_profile.get('industry', 'N/A')}
- Tone: {user_profile.get('tone', 'N/A')}
- Values: {user_profile.get('values', 'N/A')}

Incorporate this profile naturally into the content.
"""
        
        # Create tasks
        content_task = Task(
            description=f"""
Create {platform_clean} content about: {topic}

Target Audience: {audience}
Tone: {tone}
Language: {language}
{profile_context}

Platform-specific requirements:
{self._get_platform_requirements(platform_clean)}

Generate complete, ready-to-publish content.
""",
            agent=content_agent,
            expected_output=f"Complete {platform_clean} content ready for publication"
        )
        
        review_task = Task(
            description=f"""
Review the generated {platform_clean} content and validate:

1. Length is appropriate for {platform_clean}
2. Tone matches '{tone}'
3. No forbidden words or inappropriate content
4. No unsupported claims or hallucinations
5. All required elements present (hashtags, structure, etc.)

Provide validation result: APPROVED or REJECTED with specific feedback.
""",
            agent=revisor,
            expected_output="Validation result with APPROVED/REJECTED status and detailed feedback",
            context=[content_task]
        )
        
        # Create and run crew
        crew = Crew(
            agents=[content_agent, revisor],
            tasks=[content_task, review_task],
            process=Process.sequential,
            verbose=True,
            manager_llm=self.llm  # Explicitly set manager LLM
        )
        
        # Execute
        result = crew.kickoff()
        
        # Parse results
        content = content_task.output.raw if hasattr(content_task.output, 'raw') else str(content_task.output)
        review = review_task.output.raw if hasattr(review_task.output, 'raw') else str(review_task.output)
        
        # Compute accurate word count (unicode-aware)
        word_count = len(re.findall(r'\b\w+\b', content, re.UNICODE))
        
        # Additional validation with guardrails
        is_valid, errors = validate_content(content, platform_clean)
        tone_valid, tone_feedback = check_tone_consistency(content, tone)
        
        # Determine approval status
        revisor_approved = "APPROVED" in review.upper()
        fully_approved = revisor_approved and is_valid
        
        return {
            "content": content,
            "platform": platform_clean,
            "agent_used": content_agent.role,
            "model": self.model,
            "validation": {
                "approved": fully_approved,
                "revisor_approved": revisor_approved,
                "review_feedback": review,
                "guardrails_passed": is_valid,
                "guardrails_errors": errors,
                "tone_check": tone_feedback
            },
            "metadata": {
                "topic": topic,
                "audience": audience,
                "tone": tone,
                "language": language,
                "word_count": word_count
            }
        }
    
    def _get_platform_requirements(self, platform: str) -> str:
        """Get platform-specific content requirements."""
        requirements = {
            "Blog": """
- Length: 800-2000 words
- Structure: Introduction, body sections, conclusion
- Include: Compelling hook, subheadings, clear paragraphs
- SEO: Natural keyword integration
- Tone: Professional and informative
""",
            "LinkedIn": """
- Length: 150-300 words
- Structure: Hook (first 2 lines), body, call-to-action
- Include: 3-5 relevant hashtags
- Tone: Professional but personal
- Format: Short paragraphs for readability
""",
            "Twitter": """
- Length: Maximum 280 characters per tweet
- If thread: 5-7 connected tweets
- Include: 1-3 relevant hashtags
- Tone: Concise and impactful
- Format: Punchy, attention-grabbing
""",
            "Instagram": """
- Length: 100-150 words
- Structure: Hook in first line, body, hashtags at end
- Include: 10-20 hashtags, strategic emojis
- Tone: Engaging and visual
- Format: Caption that complements imagery
"""
        }
        return requirements.get(platform, "Generate appropriate content for the platform.")
