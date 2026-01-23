# Image Generator - Unsplash API Integration
"""
Module for fetching relevant images from Unsplash API based on content keywords.
"""

import os
import requests
from typing import Optional, List
import re


def extract_keywords(text: str, max_keywords: int = 3) -> List[str]:
    """
    Extract keywords from generated content for image search.
    
    Args:
        text: The generated content text
        max_keywords: Maximum number of keywords to extract
    
    Returns:
        List of keywords for image search
    """
    # Remove markdown formatting
    text = re.sub(r'[#*\[\]()]', '', text)
    
    # Split into words and filter
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    
    # Remove common stop words
    stop_words = {
        'that', 'this', 'with', 'from', 'have', 'will', 'your', 'their',
        'about', 'which', 'there', 'these', 'those', 'them', 'they', 'what',
        'when', 'where', 'would', 'could', 'should', 'been', 'being', 'into'
    }
    
    # Filter and get unique words
    keywords = [w for w in words if w not in stop_words]
    
    # Get most frequent words (simple keyword extraction)
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [word for word, _ in sorted_keywords[:max_keywords]]
    
    # If we don't have enough keywords, use the first few unique words
    if len(top_keywords) < max_keywords:
        remaining = [w for w in keywords if w not in top_keywords]
        top_keywords.extend(remaining[:max_keywords - len(top_keywords)])
    
    return top_keywords[:max_keywords]


def get_unsplash_image(query: str, api_key: Optional[str] = None) -> Optional[dict]:
    """
    Fetch a random image from Unsplash based on search query.
    
    Args:
        query: Search query (keywords)
        api_key: Unsplash API access key (optional for demo, required for production)
    
    Returns:
        Dictionary with image data: {'url': str, 'description': str, 'photographer': str}
        or None if error
    """
    # Use demo access key if no API key provided (limited requests)
    if not api_key:
        api_key = os.getenv("UNSPLASH_ACCESS_KEY")
    
    if not api_key:
        # Return None if no API key - feature will be disabled
        return None
    
    try:
        # Unsplash API endpoint
        url = "https://api.unsplash.com/photos/random"
        
        headers = {
            "Authorization": f"Client-ID {api_key}"
        }
        
        params = {
            "query": query,
            "orientation": "landscape",
            "per_page": 1
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "url": data["urls"]["regular"],
                "description": data.get("description", query),
                "photographer": data["user"]["name"],
                "photographer_url": data["user"]["links"]["html"],
                "small_url": data["urls"]["small"]  # For faster loading
            }
        else:
            print(f"Unsplash API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error fetching image from Unsplash: {e}")
        return None


def get_images_for_content(content: str, num_images: int = 1) -> List[dict]:
    """
    Extract keywords from content and fetch relevant images.
    
    Args:
        content: Generated content text
        num_images: Number of images to fetch
    
    Returns:
        List of image dictionaries
    """
    # Extract keywords
    keywords = extract_keywords(content, max_keywords=3)
    
    if not keywords:
        return []
    
    # Combine keywords for search
    search_query = " ".join(keywords)
    
    images = []
    api_key = os.getenv("UNSPLASH_ACCESS_KEY")
    
    # Fetch images (Unsplash free tier allows 50 requests/hour)
    for i in range(min(num_images, 1)):  # Limit to 1 image per request to respect rate limits
        image_data = get_unsplash_image(search_query, api_key)
        if image_data:
            images.append(image_data)
    
    return images


def format_image_markdown(image_data: dict) -> str:
    """
    Format image data as Markdown for display in Streamlit.
    
    Args:
        image_data: Dictionary with image information
    
    Returns:
        Markdown formatted string
    """
    return f"""
![{image_data['description']}]({image_data['url']})

*Photo by [{image_data['photographer']}]({image_data['photographer_url']}) on Unsplash*
"""

