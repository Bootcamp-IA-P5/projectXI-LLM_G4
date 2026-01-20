import os
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from llm_factory import get_llm


class FinancialNewsAPI:
    """Client for MarketAux Financial News API"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.marketaux.com/v1/news/all"
        self.session = requests.Session()
    
    def get_news(
        self,
        symbols: Optional[List[str]] = None,
        countries: Optional[List[str]] = None,
        industries: Optional[List[str]] = None,
        language: str = "en",
        limit: int = 10,
        sentiment_gte: Optional[float] = None,
        sentiment_lte: Optional[float] = None,
        published_after: Optional[str] = None,
        must_have_entities: bool = True
    ) -> Dict:
        """
        Fetch financial news from MarketAux API
        
        Args:
            symbols: List of stock symbols (e.g., ['AAPL', 'TSLA'])
            countries: List of country codes (e.g., ['us', 'ca'])
            industries: List of industries (e.g., ['Technology', 'Finance'])
            language: Language code (default: 'en')
            limit: Number of articles to return
            sentiment_gte: Minimum sentiment score
            sentiment_lte: Maximum sentiment score
            published_after: Filter articles published after this date
            must_have_entities: Only return articles with identified entities
        
        Returns:
            Dictionary containing news data
        """
        params = {
            "api_token": self.api_token,
            "language": language,
            "limit": limit,
            "must_have_entities": must_have_entities,
            "sort": "published_at",
            "sort_order": "desc"
        }
        
        if symbols:
            params["symbols"] = ",".join(symbols)
        if countries:
            params["countries"] = ",".join(countries)
        if industries:
            params["industries"] = ",".join(industries)
        if sentiment_gte is not None:
            params["sentiment_gte"] = sentiment_gte
        if sentiment_lte is not None:
            params["sentiment_lte"] = sentiment_lte
        if published_after:
            params["published_after"] = published_after
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching news: {e}")
            return {"data": [], "meta": {"found": 0, "returned": 0}}


def format_news_article(article: Dict) -> str:
    """Format a news article for display"""
    formatted = f"### {article.get('title', 'No Title')}\n\n"
    
    # Handle source - it can be a string or dict
    source = article.get('source', {})
    if isinstance(source, str):
        source_name = source
    else:
        source_name = source.get('name', 'Unknown')
    
    formatted += f"**Source:** {source_name}\n"
    formatted += f"**Published:** {format_date(article.get('published_at'))}\n"
    
    if article.get('description'):
        formatted += f"\n{article.get('description')}\n"
    
    if article.get('url'):
        formatted += f"\n[Read more]({article.get('url')})\n"
    
    # Add entities information
    entities = article.get('entities', [])
    if entities:
        formatted += "\n**Entities:**\n"
        for entity in entities[:5]:  # Limit to first 5 entities
            symbol = entity.get('symbol', '')
            name = entity.get('name', '')
            sentiment = entity.get('sentiment_score', 0)
            sentiment_emoji = "📈" if sentiment > 0 else "📉" if sentiment < 0 else "➡️"
            formatted += f"- {sentiment_emoji} **{symbol}** {name} (Sentiment: {sentiment:.2f})\n"
    
    formatted += "\n---\n"
    return formatted


def format_date(date_str: str) -> str:
    """Format date string for display"""
    try:
        if not date_str:
            return "Unknown"
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M UTC')
    except:
        return date_str


def get_news_summary(news_articles: List[Dict], llm, language: str = "en") -> str:
    """Generate AI summary of news articles using the configured LLM"""
    if not news_articles:
        return "No articles to summarize."
    
    # Prepare articles text for summarization
    articles_text = "\n\n".join([
        f"Title: {article.get('title', '')}\n"
        f"Description: {article.get('description', '')}\n"
        f"Entities: {', '.join([e.get('symbol', '') for e in article.get('entities', [])])}"
        for article in news_articles[:5]  # Limit to first 5 articles
    ])
    
    # Create summary prompt based on language
    if language == "es":
        prompt = f"""Como analista financiero, resume las siguientes noticias financieras en un análisis conciso:

{articles_text}

Proporciona:
1. Resumen ejecutivo (2-3 frases)
2. Tendencias clave identificadas
3. Entidades más mencionadas y su sentimiento
4. Implicaciones para el mercado

Responde en español."""
    else:
        prompt = f"""As a financial analyst, summarize the following financial news articles:

{articles_text}

Provide:
1. Executive summary (2-3 sentences)
2. Key trends identified
3. Most mentioned entities and their sentiment
4. Market implications

Respond in English."""
    
    try:
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error generating summary: {e}"


def get_popular_symbols() -> List[Dict[str, str]]:
    """Return list of popular stock symbols for selection"""
    return [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "GOOGL", "name": "Alphabet Inc."},
        {"symbol": "AMZN", "name": "Amazon.com Inc."},
        {"symbol": "TSLA", "name": "Tesla Inc."},
        {"symbol": "META", "name": "Meta Platforms Inc."},
        {"symbol": "NVDA", "name": "NVIDIA Corporation"},
        {"symbol": "JPM", "name": "JPMorgan Chase & Co."},
        {"symbol": "V", "name": "Visa Inc."},
        {"symbol": "JNJ", "name": "Johnson & Johnson"}
    ]


def get_popular_industries() -> List[str]:
    """Return list of popular industries for filtering"""
    return [
        "Technology",
        "Finance",
        "Healthcare",
        "Consumer Discretionary",
        "Energy",
        "Industrials",
        "Materials",
        "Real Estate",
        "Utilities",
        "Communication Services"
    ]


def get_country_options() -> List[Dict[str, str]]:
    """Return list of country options"""
    return [
        {"code": "us", "name": "United States"},
        {"code": "ca", "name": "Canada"},
        {"code": "gb", "name": "United Kingdom"},
        {"code": "de", "name": "Germany"},
        {"code": "fr", "name": "France"},
        {"code": "jp", "name": "Japan"},
        {"code": "cn", "name": "China"},
        {"code": "au", "name": "Australia"},
        {"code": "in", "name": "India"},
        {"code": "br", "name": "Brazil"}
    ]


def validate_api_key(api_token: str) -> bool:
    """Validate MarketAux API key with a simple test request"""
    if not api_token:
        return False
    
    try:
        test_api = FinancialNewsAPI(api_token)
        result = test_api.get_news(limit=1)
        return result.get("meta", {}).get("returned", 0) > 0
    except:
        return False


def render_financial_news_tab():
    """Render the Financial News tab in Streamlit"""
    
    # Initialize session state variables
    if "summary_requested" not in st.session_state:
        st.session_state.summary_requested = False
    
    st.header("📈 Financial News & Market Intelligence")
    st.caption("Real-time financial news with AI-powered analysis")

    # ==============================
    # API KEY CHECK
    # ==============================
    api_token = os.getenv("MARKETAUX_API_KEY")
    if not api_token:
        st.error("❌ MARKETAUX_API_KEY not found in environment variables.")
        st.info("🔑 Get your free API key at: https://www.marketaux.com/register")
        st.info("Add it to your .env file: MARKETAUX_API_KEY=your_key_here")
        return

    news_api = FinancialNewsAPI(api_token)

    # ==============================
    # SIDEBAR FILTERS
    # ==============================
    with st.sidebar:
        st.subheader("🔍 News Filters")

        popular_symbols = get_popular_symbols()
        symbol_options = [f"{s['symbol']} - {s['name']}" for s in popular_symbols]
        selected_symbols = st.multiselect(
            "Stock Symbols",
            options=symbol_options,
            key="news_symbols"
        )
        symbols = [s.split(" - ")[0] for s in selected_symbols]

        country_options = get_country_options()
        country_names = [c["name"] for c in country_options]
        selected_countries = st.multiselect(
            "Countries",
            options=country_names,
            default=["United States"],
            key="news_countries"
        )
        countries = [
            c["code"] for c in country_options if c["name"] in selected_countries
        ]

        industries = st.multiselect(
            "Industries",
            options=get_popular_industries(),
            key="news_industries"
        )

        st.subheader("📊 Sentiment")
        sentiment_filter = st.selectbox(
            "Sentiment Filter",
            ["All", "Positive Only", "Negative Only", "Neutral Only"],
            key="news_sentiment"
        )

        language = st.selectbox(
            "Language",
            ["en", "es"],
            format_func=lambda x: "English" if x == "en" else "Español",
            key="news_language"
        )

        limit = st.slider(
            "Articles",
            min_value=5,
            max_value=50,
            value=10,
            key="news_limit"
        )

        days_back = st.slider(
            "Days Back",
            min_value=1,
            max_value=30,
            value=7,
            key="news_days_back"
        )

        published_after = (
            datetime.now() - timedelta(days=days_back)
        ).strftime("%Y-%m-%d")

    # ==============================
    # LAYOUT
    # ==============================
    col1, col2 = st.columns([2, 1])

    # Persistent containers (CRITICAL)
    with col1:
        st.subheader("📰 Latest Financial News")
        news_container = st.container()

    with col2:
        st.subheader("🤖 AI Analysis")
        summary_container = st.container()

    # ==============================
    # FETCH NEWS
    # ==============================
    if st.button("🔄 Fetch News", type="primary", key="fetch_news"):
        with st.spinner("Fetching financial news..."):
            sentiment_gte, sentiment_lte = None, None
            if sentiment_filter == "Positive Only":
                sentiment_gte = 0.1
            elif sentiment_filter == "Negative Only":
                sentiment_lte = -0.1
            elif sentiment_filter == "Neutral Only":
                sentiment_gte, sentiment_lte = -0.1, 0.1

            news_data = news_api.get_news(
                symbols=symbols or None,
                countries=countries or None,
                industries=industries or None,
                language=language,
                limit=limit,
                sentiment_gte=sentiment_gte,
                sentiment_lte=sentiment_lte,
                published_after=published_after,
            )

            st.session_state.news_data = news_data
            st.session_state.news_fetched = True
            st.session_state.generate_summary = False

    # ==============================
    # RENDER NEWS (SAFE)
    # ==============================
    with news_container:
        news_container.empty()

        if st.session_state.get("news_fetched"):
            articles = st.session_state.news_data.get("data", [])

            if articles:
                st.success(f"✅ {len(articles)} articles found")
                for article in articles:
                    st.markdown(format_news_article(article))
            else:
                st.warning("No articles found.")

    # ==============================
    # AI SUMMARY
    # ==============================
    if st.session_state.get("news_fetched"):
        if st.button("📋 Generate AI Summary", key="generate_summary_button"):
            # Use a different session state variable name
            st.session_state.summary_requested = True

    with summary_container:
        summary_container.empty()

        if st.session_state.get("summary_requested"):
            articles = st.session_state.news_data.get("data", [])

            if not articles:
                st.info("No articles available for summarization.")
            else:
                try:
                    llm = get_llm(
                        st.session_state.llm_provider,
                        st.session_state.llm_model,
                        st.session_state.llm_temperature,
                    )

                    with st.spinner("Generating AI analysis..."):
                        summary = get_news_summary(articles, llm, language)
                        st.markdown(summary)

                except Exception as e:
                    st.error(f"❌ LLM Error: {e}")
