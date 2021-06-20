import asyncio
from pyppeteer import launch
import time

async def getTestPage():

    browser = await launch()
    page = await browser.newPage()

    # B0
    url = 'https://pdglive.lbl.gov/Particle.action?init=0&node=S042&home=MXXX045'

    # phi
    # url = 'https://pdglive.lbl.gov/Particle.action?init=0&node=M004&home=MXXX005'

    await page.goto(url)

    # js = "getParticleSection('./Particle.action', 'section_S042212', 'S042212', 'S042')"
    js = "getDecayClump('./Particle.action', 'clump_E', 'E', 'S042','MXXX045');"

    eval = await page.evaluate(js)

    # Wait for the JS to evaluate zzzzz....
    time.sleep(5)

    html = await page.content()

    await page.screenshot({'path': 'example.png', 'fullPage' : True})

    print(html)

    await browser.close()

    f = open('testPDGLight.html', 'w')

    f.write(html)
    f.close()

if __name__ == '__main__':

    asyncio.get_event_loop().run_until_complete(getTestPage())
