import asyncio
import aiohttp
from bs4 import BeautifulSoup
import sqlite3


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:

        urls = [
            'https://www.inf-schule.de/',
            'https://www.google.com/',
            "https://mpg-trier.de/"
        ]

        tasks = [fetch(session, url) for url in urls]

        html_pages = await asyncio.gather(*tasks)

        conn = sqlite3.connect('results.db')
        c = conn.cursor()

        
        c.execute('''CREATE TABLE IF NOT EXISTS results (title TEXT, url TEXT, content TEXT)''')

        for i, html in enumerate(html_pages):
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title').text
            data = soup.find_all("h2")
            c.execute('''INSERT INTO results VALUES (?, ?, ?)''', (title, urls[i], str(data)))
            
        conn.commit()
        conn.close() 

asyncio.run(main(), debug=True)
