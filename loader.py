# from llama_index import download_loader

# SimpleWebPageReader = download_loader("SimpleWebPageReader")

# def web_page_reader(url):
#     loader = SimpleWebPageReader()
#     documents = loader.load_data(urls=[url])
#     return documents

# loader = SimpleWebPageReader()
# documents = loader.load_data(urls=['https://google.com'])

# web_page_reader('https://www.health.go.ke/node/708')

from bs4 import BeautifulSoup as soup
import requests
from llama_index import Document
from llama_index import SimpleDirectoryReader


urls = [
    "https://www.sicklecelldisease.org/get-involved/events/national-sickle-cell-awareness-month/#:~:text=September%20is%20National%20Sickle%20Cell,Awareness%20Month%20Flyer%20%26%20Facts%20Sheet.",
    "https://nation.africa/kenya/health/ministry-advises-couples-to-test-for-sickle-cell-before-getting-children-4277778",
    "https://www.the-star.co.ke/health/2023-09-13-sickle-cell-stigma-moh-to-focus-on-community-awareness/",
]



def web_page_reader(urls=urls):
    docs = []
    for url in urls:
        try:
            response = requests.get(url)
            page = soup(response.content, "lxml")
            text = page.text
            
            docs.append(Document(
                text=text,
                extra_info={"source_url": url}
            ))
        except Exception as e:
            print(e)

    return docs


docs = web_page_reader(urls)

def load_directory(folder_path="storage/"):
    reader = SimpleDirectoryReader(folder_path, recursive=True)
    documents = reader.load_data()
    
    return documents
    

if __name__ == "__main__":
    docs = web_page_reader(urls)
    print(docs)
    docs = load_directory()
    print(docs)