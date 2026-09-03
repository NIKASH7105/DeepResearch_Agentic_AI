"""
Image search tool using DuckDuckGo
"""
import httpx
import logging
from typing import List, Dict
from ddgs import DDGS
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class ImageSearchTool:
    """Search and download images from the web"""
    
    def __init__(self, cache_dir: str = "./temp/images"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def search_images(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for images related to query
        
        Args:
            query: Search query for images
            max_results: Maximum number of images to find
            
        Returns:
            List of image data with url, title, thumbnail
        """
        max_retries = 2
        for attempt in range(max_retries):
            try:
                logger.info(f"[ImageSearch] Searching images for: {query} (attempt {attempt + 1}/{max_retries})")
                
                # Create new DDGS instance and search
                with DDGS(timeout=30) as ddgs:
                    results = []
                    
                    # ddgs.images() returns a generator, convert to list
                    image_results = list(ddgs.images(
                        query,
                        max_results=max_results * 3  # Get more to increase success rate
                    ))
                    
                    logger.info(f"[ImageSearch] Found {len(image_results)} images")
                    
                    for result in image_results:
                        if isinstance(result, dict):
                            results.append({
                                'title': result.get('title', 'Image'),
                                'url': result.get('image', ''),
                                'thumbnail': result.get('thumbnail', ''),
                                'source': result.get('source', '')
                            })
                    
                    if results:
                        return results[:max_results * 2]
                    
            except Exception as e:
                logger.warning(f"[ImageSearch] Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(1)
                else:
                    logger.error("[ImageSearch] All attempts failed")
                    import traceback
                    traceback.print_exc()
        
        return []
    
    async def download_image(self, url: str, filename: str) -> str:
        """
        Download image from URL
        
        Args:
            url: Image URL
            filename: Filename to save as
            
        Returns:
            Path to downloaded image or empty string if failed
        """
        try:
            filepath = self.cache_dir / filename
            
            # Skip if already downloaded
            if filepath.exists():
                logger.info(f"[ImageSearch] Using cached image: {filename}")
                return str(filepath)
            
            logger.info(f"[ImageSearch] Downloading: {url[:60]}...")
            
            # Download image with better headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with httpx.AsyncClient(
                timeout=20.0, 
                follow_redirects=True,
                headers=headers
            ) as client:
                response = await client.get(url)
                
                if response.status_code == 200 and len(response.content) > 1000:
                    # Save image
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"[ImageSearch] Downloaded: {filename} ({len(response.content)} bytes)")
                    return str(filepath)
                else:
                    logger.warning(f"[ImageSearch] Invalid response: {response.status_code}, size: {len(response.content)}")
                    
        except Exception as e:
            logger.error(f"[ImageSearch] Download error for {filename}: {e}")
        
        return ""
    
    async def search_and_download(self, query: str, session_id: str, max_images: int = 3) -> List[str]:
        """
        Search for images and download them
        
        Args:
            query: Search query
            session_id: Session ID for unique filenames
            max_images: Maximum images to download
            
        Returns:
            List of downloaded image paths
        """
        logger.info(f"[ImageSearch] Starting image search and download for: {query}")
        
        # Search for images
        image_results = self.search_images(query, max_results=max_images)
        
        if not image_results:
            logger.warning("[ImageSearch] No images found from search")
            return []
        
        downloaded_images = []
        
        # Try to download images
        for idx, img in enumerate(image_results):
            if len(downloaded_images) >= max_images:
                break
            
            # Try primary URL first, then thumbnail
            url = img.get('url') or img.get('thumbnail')
            if not url:
                logger.warning(f"[ImageSearch] No URL for image {idx}")
                continue
            
            filename = f"{session_id}_img_{len(downloaded_images)}.jpg"
            filepath = await self.download_image(url, filename)
            
            if filepath:
                downloaded_images.append(filepath)
            else:
                # Try thumbnail as fallback
                thumbnail = img.get('thumbnail')
                if thumbnail and thumbnail != url:
                    logger.info("[ImageSearch] Trying thumbnail URL as fallback...")
                    filepath = await self.download_image(thumbnail, filename)
                    if filepath:
                        downloaded_images.append(filepath)
        
        logger.info(f"[ImageSearch] Successfully downloaded {len(downloaded_images)}/{max_images} images")
        return downloaded_images


# Global instance
image_search_tool = ImageSearchTool()
