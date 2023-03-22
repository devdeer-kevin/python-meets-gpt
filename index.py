import asyncio
import aiohttp
from bs4 import BeautifulSoup
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def scrape_page(page_num):
    url = f"https://www.ebay-kleinanzeigen.de/s-iphone-14-pro-schwarz/k0?page={page_num}"
    html = await fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text() # Extrahiere den Text aus dem HTML-Code
    prompt = "Findest du hier ein iPhone 14 Pro unter 900 EURO? Falls nicht, antworte einfach nur mit dem Wort NEIN. Hier ist der Text der Website:" + "\n" + text
    response = await openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=256,
        n=1,
        stop=None,
        temperature=0.5,
    )
    output_text = response.choices[0].text.strip()
    print(output_text)

async def main():
    tasks = []
    for page_num in range(1, 6):
        tasks.append(asyncio.create_task(scrape_page(page_num)))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())