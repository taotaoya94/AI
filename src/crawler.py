import requests
import time
import logging
import random
from typing import Optional, Dict, List
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InequalityCrawler:
    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.ua = UserAgent()
        self.session = requests.Session()
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def _make_request(self, url: str) -> Optional[str]:
        try:
            time.sleep(self.delay)
            response = self.session.get(
                url,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {str(e)}")
            return None
    
    def crawl_baidu_baike(self, name: str) -> Optional[Dict]:
        encoded_name = quote(name)
        url = f"https://baike.baidu.com/item/{encoded_name}"
        html = self._make_request(url)
        
        if not html:
            return None
        
        try:
            soup = BeautifulSoup(html, 'lxml')
            result = {
                'source': 'baidu_baike',
                'name': name,
                'description': '',
                'math_form': '',
                'content': []
            }
            
            summary = soup.find('div', class_='lemma-summary')
            if summary:
                result['description'] = summary.get_text(strip=True)
            
            main_content = soup.find('div', class_='main-content')
            if main_content:
                paras = main_content.find_all(['div', 'p'], class_='para')
                for para in paras[:10]:
                    text = para.get_text(strip=True)
                    if text:
                        result['content'].append(text)
            
            return result
        except Exception as e:
            logger.error(f"Error parsing Baidu Baike for {name}: {str(e)}")
            return None
    
    def crawl_wikipedia_zh(self, name: str) -> Optional[Dict]:
        encoded_name = quote(name)
        url = f"https://zh.wikipedia.org/wiki/{encoded_name}"
        html = self._make_request(url)
        
        if not html:
            return None
        
        try:
            soup = BeautifulSoup(html, 'lxml')
            result = {
                'source': 'wikipedia_zh',
                'name': name,
                'description': '',
                'math_form': '',
                'content': []
            }
            
            content_div = soup.find('div', {'id': 'mw-content-text'})
            if content_div:
                first_para = content_div.find('p', recursive=False)
                if first_para:
                    result['description'] = first_para.get_text(strip=True)
                
                paragraphs = content_div.find_all('p', limit=15)
                for para in paragraphs:
                    text = para.get_text(strip=True)
                    if text and len(text) > 20:
                        result['content'].append(text)
            
            return result
        except Exception as e:
            logger.error(f"Error parsing Wikipedia ZH for {name}: {str(e)}")
            return None
    
    def crawl_wikipedia_en(self, name_en: str) -> Optional[Dict]:
        encoded_name = quote(name_en)
        url = f"https://en.wikipedia.org/wiki/{encoded_name}"
        html = self._make_request(url)
        
        if not html:
            return None
        
        try:
            soup = BeautifulSoup(html, 'lxml')
            result = {
                'source': 'wikipedia_en',
                'name': name_en,
                'description': '',
                'math_form': '',
                'content': []
            }
            
            content_div = soup.find('div', {'id': 'mw-content-text'})
            if content_div:
                first_para = content_div.find('p', recursive=False)
                if first_para:
                    result['description'] = first_para.get_text(strip=True)
                
                paragraphs = content_div.find_all('p', limit=15)
                for para in paragraphs:
                    text = para.get_text(strip=True)
                    if text and len(text) > 20:
                        result['content'].append(text)
            
            return result
        except Exception as e:
            logger.error(f"Error parsing Wikipedia EN for {name_en}: {str(e)}")
            return None
    
    def crawl_inequality(self, name: str, english_name: Optional[str] = None) -> List[Dict]:
        logger.info(f"Crawling data for: {name}")
        results = []
        
        baidu_result = self.crawl_baidu_baike(name)
        if baidu_result:
            results.append(baidu_result)
        
        wiki_zh_result = self.crawl_wikipedia_zh(name)
        if wiki_zh_result:
            results.append(wiki_zh_result)
        
        if english_name:
            wiki_en_result = self.crawl_wikipedia_en(english_name)
            if wiki_en_result:
                results.append(wiki_en_result)
        
        return results
