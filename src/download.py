from bs4 import BeautifulSoup as soup
import requests
from urllib.parse import urljoin

# Trying to make a general download script that can be customized as needed
def get_links(url, link_selector):
    """get_links(url: String, link_selector: String)
    Returns a list of url's that match the given selector on a page. Used for getting all candidates from a list of candidates.
    url should be the url that is requested to get a webpage listing candidates.
    link_selector should be the CSS selector of the link that links to the candidate page.
    """
    data = requests.get(url)
    page = soup(data.text, 'html.parser')

    print("Scanning " + page.title.string + "...")
    links = list()
    for link in page.select(link_selector):
        # Using urljoin to ensure that links are proper links, as some pages may give relative links
        links.append(urljoin(url, link['href']))
    
    return links

def get_page_values(url, selectors):
    """get_desc_img(url: String, selectors: iter((String, String)))
    url should be the url that is requested to get a webpage listing candidates.
    selectors should be an iterable of tuples, the first being a selector, the second being an attribute to return
    for each one it will be searched for, and if it exists the first result will have it's attribute placed in the list
    otherwise None will be inserted, and this list will be returned
    """
    data = requests.get(url)
    page = soup(data.text, 'html.parser')

    print("Scanning " + page.title.string + "...")
    
    results = list()
    for selector in selectors:
        search = page.select(selector[0])
        
        result = None
        if len(search):
            if selector[1]:
                result = search[0].get(selector[1])
                if result is not None and (selector[1] == "src" or selector[1] == "href"):
                    result = urljoin(url, result)
                
            else:
                result = search[0].get_text()
        results.append(result)
    
    return results