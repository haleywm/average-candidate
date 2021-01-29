import scraper

#links = download.get_links("https://greens.org.au/wa/state-candidates", "a.person-box")
#links = download.get_links("https://www.waliberal.org.au/state-candidates/", "a.more-link")

#data = download.get_page_values("https://greens.org.au/wa/person/alison-xamon-0", [("h1.hero-image-title", None), ("div.text-formatted", None), ("div.person-contact img", "src")])

scraper.scrape(["https://greens.org.au/wa/state-candidates"], "a.person-box", "div.person-contact img", "h1.hero-image-title", "div.text-formatted", "greens")