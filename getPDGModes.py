import re

from tqdm import tqdm

from bs4 import BeautifulSoup

def getRawModes(fileName):

    f = open(fileName, 'r')

    soup = BeautifulSoup(f, 'html.parser')

    # Find JS to open *all* dropdowns

    # for link in soup.find_all('a'):
    #     js = link.get('onclick')
    #     if js and js[:3] == 'get':
    #         print(js)
    #
    # for link in soup.find_all('script'):
    #     print(link)

    for i, link in enumerate(soup.find_all("tr")):

        if not 'gamma' in str(link):
            continue

        padPrev = 0
        parentDecays = []

        for t in link.find_all("td"):
            scripts = t.find_all("script")

            if len(scripts) >= 3 and 'Gamma' in str(scripts[0]):

                pad = 0
                padMatch = re.search('<td style="padding-left: ([0-9][0-9])px;">', str(t))
                if padMatch:
                    pad = int(padMatch.group(1))

                gamma = -1
                gammaMatch = padMatch = re.search('\\\\Gamma_{([0-9].*)}', str(scripts[0]))
                if gammaMatch:
                    gamma = int(gammaMatch.group(1))
                else:
                    continue

                if padPrev < pad:
                    parentDecays.append(gamma - 1)
                if padPrev > pad:
                    parentDecays.pop()

                padPrev = pad

                print('Subdecay : ', parentDecays)

                print('Gamma : ', scripts[0])
                print('Padding : ', pad)
                print('Contents :', scripts[1:-1])
                print('BF : ', scripts[-1])
                print('')

        return

        print('')

if __name__ == '__main__':

    getRawModes('testPDG.html')
