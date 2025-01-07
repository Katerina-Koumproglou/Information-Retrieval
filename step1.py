import requests
from bs4 import BeautifulSoup
import json

#Συνάρτηση για να ανακτήσουμε συγκεκριμένα άρθρα
def fetch_articles(start_url, num_articles = 10):
    base_url = "https://en.wikipedia.org/"
    visited = set() #Σύνολο url τα οποία έχουμε ήδη επισκεφτεί
    articles = [] #Δεδομένα των άρθρων
    
    #Συνάρτηση για να συλλέξουμε τα δεδομένα της κάθε σελίδας
    def fetch_article_data(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1').text
        paragraphs = soup.find_all('p')
        content = " ".join([p.text for p in paragraphs])
        return {"title": title, "url": url, "content": content}
    
    #Τα url τα οποία θα επισκεφτούμε στην συνέχεια
    to_visit = [start_url]
    while to_visit and len(articles) < num_articles:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue
        visited.add(current_url)
        
        #Αποφεύγουμε το Main Page της Wikipedia
        if 'Main_Page' in current_url:
            continue
        
        print(f"Fetching: {current_url}")
        article = fetch_article_data(current_url)
        if article:
            articles.append(article)
        
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href = True):
            href = link['href']
            if href.startswith('/wiki/') and ':' not in href:
                full_url = base_url + href
                if full_url not in visited:
                    to_visit.append(full_url)
        
    return articles
        

start_url = "https://en.wikipedia.org/wiki/Processor_(computing)"
articles = fetch_articles(start_url, num_articles = 9)

with open("articles.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)
print("The data has been saved to \"articles.json\"")