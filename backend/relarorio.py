
# web_search_agent.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from openai import OpenAI
from enum import Enum





class InsightCategory(str, Enum):
    """Categories for player insights"""
    PLAYING_STYLE = "playing_style"  # How the player plays/approaches the game
    STRENGTHS = "strengths"          # Specific strengths observed
    WEAKNESSES = "weaknesses"        # Areas for improvement
    TECHNIQUE = "technique"          # Technical abilities and skills
    TACTICAL = "tactical"            # Tactical understanding and positioning
    PHYSICAL = "physical"            # Physical attributes and traits
    MENTAL = "mental"                # Mental aspects and decision-making
    DEVELOPMENT = "development"      # Development trajectory/potential
    CHARACTER = "character"          # Personality and character traits
    INJURY = "injury"                # Injury history/concerns
    TRANSFER = "transfer"            # Transfer information/market value
class Source(BaseModel):
    """Information source from web search"""
    url: str = Field(..., description="URL of the source")
    title: Optional[str] = Field(None, description="Title of the source")
    source_name: Optional[str] = Field(None, description="Name of the publication/source")
    publication_date: Optional[str] = Field(None, description="Publication date")
    relevance: float = Field(..., description="Relevance to the player (0.0-1.0)")
    summary: str = Field(..., description="Brief summary of the source content")
    content_for_report: List[str] = Field(..., description="Content extracted from the URL for the report")
    keywords: List[str] = Field(..., description="Keywords categorizing the content")

class PlayerInsight(BaseModel):
    """A specific insight about a player extracted from sources"""
    category: InsightCategory = Field(..., description="Category of the insight")
    insight: str = Field(..., description="The specific insight or observation")
    source_url: str = Field(..., description="URL of the source this came from")
    source_name: str = Field(..., description="Name of the publication/source")
    relevance: float = Field(1.0, description="Relevance score (0.0-1.0)")
    confidence: float = Field(1.0, description="Confidence in the insight (0.0-1.0)")
    
class CategorySummary(BaseModel):
    """Summary of insights for a specific category"""
    category: str = Field(..., description="Category name")
    summary: str = Field(..., description="Synthesized summary of insights in this category")
    key_points: List[str] = Field(..., description="Key points extracted from insights")
    consensus_level: float = Field(..., description="Level of consensus among sources (0.0-1.0)")

class CuratedPlayerResearch(BaseModel):
    """Organized research with insights categorized"""
    player_name: str = Field(..., description="Player name")
    player_summary: str = Field(..., description="Overall player summary")
    sources: List[Source] = Field(..., description="All sources used")
    category_summaries: Dict[str, CategorySummary] = Field(..., description="Summaries by category")
    top_sources: List[str] = Field(..., description="IDs of most valuable sources")
    curation_timestamp: datetime = Field(..., description="When curation was performed")


class WebSearchResult(BaseModel):
    """Raw results from web search"""
    player_name: str = Field(..., description="Player name that was searched for")
    urls_searched: List[Source] = Field(..., description="List of URLs searched with their content")
    search_query: Optional[str] = Field(None, description="Query used for the search")
    timestamp: Optional[datetime] = Field(None, description="When the search was performed")

class WebSearchAgent:
    """Agent responsible for finding qualitative information about players online"""
    
    def __init__(self, api_key=None):
        """Initialize the web search agent"""
        # Load API key from environment variable
        openai_api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=openai_api_key)
    
    def search_player_info(self, player_name: str, player_context: Optional[Dict] = None) -> WebSearchResult:
        """
        Search for qualitative information about a player online
        
        Args:
            player_name: Name of the player to search for
            player_context: Optional context about the player (position, team, etc.)
            
        Returns:
            WebSearchResult with sources found
        """
        # Create context prompt with player information
        context_text = ""
        if player_context:
            positions = player_context.get("positions", [])
            position_text = ", ".join([p.get("position", {}).get("name", "") for p in positions]) if positions else ""
            team = player_context.get("currentTeamId", "")
            
            context_text = f"Player information: Position(s): {position_text}, Team ID: {team}"
        
        # Define search system prompt
        system_prompt = """You are a specialized football scout researcher focused on finding SUBJECTIVE, QUALITATIVE information about players that complements statistical data.

MISSION:
Find information that can ONLY be obtained by WATCHING THE PLAYER in matches - observations that no database of statistics could capture.

YOUR FOCUS:
1. Technical abilities visible only to the trained eye
2. Decision-making nuances
3. Off-ball movement and positioning
4. Psychological and character traits
5. Tactical understanding

SEARCH GUIDELINES:
1. PRIORITIZE these source types:
   - Detailed match analyses from tactical experts
   - Scouting reports with specific examples
   - Coach and professional scout interviews/quotes
   - In-depth player profile articles with specific observations
   - Expert analyst commentary with specific examples

2. For each source found, extract:
   - URL and basic metadata (title, source name, date)
   - Brief summary of the source's content
   - 3-5 key content snippets that provide subjective observations
   - Keywords that categorize the type of content

3. AVOID:
   - Sources that only repeat statistical information
   - Generic praise without specific observations
   - Fan opinions without expert backing
   - Outdated assessments (over 18 months old)

FORMAT YOUR RESULTS as a structured list of sources with their extracted content."""

        # Define user prompt
        user_prompt = f"""Find detailed SUBJECTIVE OBSERVATIONS about {player_name} that would complement statistical data.

Focus specifically on information that could ONLY be obtained by watching the player in matches - technical details, decision-making, off-ball movement, psychological traits, and tactical understanding that statistics cannot capture."""
        
        if context_text:
            user_prompt += f"\n\n{context_text}"
        
        # Execute search using OpenAI with Responses API
        try:
            response = self.client.responses.parse(
                model="gpt-4o",
                tools=[{"type": "web_search_preview", "search_context_size": "high"}],
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                text_format=WebSearchResult
            )
            
            # Extract the parsed model directly
            result = response.output[0].content[0].parsed
            
            # Set the search query and timestamp
            result.search_query = user_prompt
            result.timestamp = datetime.now()
            
            return result
            
        except Exception as e:
            print(f"Error performing web search: {e}")
            # Return minimal valid result in case of error
            return WebSearchResult(
                player_name=player_name,
                urls_searched=[],
                search_query=user_prompt,
                timestamp=datetime.now()
            )
        
class CuratorAgent:
    """Agent responsible for curating and organizing player research"""
    
    def __init__(self, api_key=None):
        """Initialize the curator agent"""
        # Load API key from environment variable
        openai_api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=openai_api_key)
        self.system_prompt = """You are a professional football scouting curator specialized in extracting structured insights from research.

MISSION:
Transform raw information from multiple sources into categorized, structured insights about football players.

YOUR CAPABILITIES:
- Extract specific, meaningful insights from source content
- Categorize insights into appropriate categories
- Eliminate duplicate or redundant information
- Identify and resolve contradictions between sources 
- Assess reliability and relevance of information
- Synthesize multiple insights into coherent summaries
- Perform targeted additional research on specific URLs when needed

EXTRACTION GUIDELINES:
[... rest of extraction guidelines as before ...]

FOCUSED RESEARCH GUIDELINES:
1. When you find interesting claims or partial information, explore the provided URLs more deeply
2. Focus on examining the original sources more thoroughly rather than searching for new sources
3. When exploring a URL, look specifically for:
   - More detailed explanations of techniques or traits mentioned
   - Supporting examples of claims made
   - Context around quotes or observations
   - Information about the time period of the observation
4. Prioritize deeper understanding of existing sources over finding new ones

FORMAT YOUR OUTPUT as structured insights according to the provided schema.
"""
    
    def curate_player_research(self, web_search_result: WebSearchResult) -> CuratedPlayerResearch:
        """
        Process web search results into structured, categorized insights
        
        Args:
            web_search_result: Raw results from web search
            
        Returns:
            Curated research with structured insights
        """
        player_name = web_search_result.player_name
        
        # Format the sources for the prompt
        sources_text = ""
        for i, source in enumerate(web_search_result.urls_searched, 1):
            sources_text += f"\nSOURCE {i}: {source.url}\n"
            sources_text += f"TITLE: {source.title}\n"
            sources_text += f"SOURCE: {source.source_name}\n"
            sources_text += f"DATE: {source.publication_date}\n"
            sources_text += f"SUMMARY: {source.summary}\n"
            sources_text += "CONTENT EXTRACTS:\n"
            for j, content in enumerate(source.content_for_report, 1):
                sources_text += f"- {content}\n"
            sources_text += f"KEYWORDS: {', '.join(source.keywords)}\n"
        
        # Extract just the URLs for reference
        urls_list = [source.url for source in web_search_result.urls_searched]
        urls_text = "\n".join(urls_list)
        
        # Create the user prompt
        user_prompt = f"""Process these web search results about {player_name} into structured insights:

{sources_text}

Extract specific insights about the player, categorize them properly, and synthesize the information into category summaries and an overall player summary.

Focus on insights that provide subjective observations about the player's abilities, style, and characteristics that wouldn't be captured by statistics alone.

If you need additional information to better understand or verify claims, you can explore these URLs more deeply:
{urls_text}

Prioritize deeper exploration of these existing sources rather than searching for entirely new information.
"""
        
        try:
            # Use OpenAI with web search enabled but medium context
            response = self.client.responses.parse(
                model="gpt-4o",
                tools=[{"type": "web_search_preview", "search_context_size": "medium"}],
                input=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                text_format=CuratedPlayerResearch
            )
            
            # Extract the parsed model
            result = response.output[0].content[0].parsed
            
            # Update timestamp
            result.curation_timestamp = datetime.now()
            
            return result
            
        except Exception as e:
            print(f"Error curating player research: {e}")
            # Return minimal valid response in case of error
            return CuratedPlayerResearch(
                player_name=player_name,
                player_summary=f"Error processing research for {player_name}: {str(e)}",
                insights=[],
                category_summaries={},
                recommended_sources=[]
            )
        


researcher = WebSearchAgent()
research = researcher.search_player_info("Rafael Leão")
curator = CuratorAgent()
curated = curator.curate_player_research(research)
print(curated.player_name)
print(curated.player_summary)   
print(curated.insights)
print(curated.category_summaries)
print(curated.recommended_sources)
print(curated.curation_timestamp)
