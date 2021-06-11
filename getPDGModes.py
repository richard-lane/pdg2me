import re

from tqdm import tqdm

from bs4 import BeautifulSoup

# Regex to match arbitrary excited resonances?
# Function to build antiparticle from particle (+ vice versa?)

particleNames = {

r'{{\mathit X}}' : 'X',
r'{{\mathit X}_{{c}}}' : 'Xc',
r'{{\mathit X}_{{b}}}' : 'Xb',

r'{{\mathit \ell}^{+}}' : 'lepton+',
r'{{\mathit \ell}^{-}}' : 'lepton-',

r'{{\mathit e}^{+}}' : 'e+',
r'{{\mathit e}^{-}}' : 'e-',

r'{{\mathit \mu}^{+}}' : 'mu+',
r'{{\mathit \mu}^{-}}' : 'mu-',

r'{{\mathit \tau}^{+}}' : 'tau+',
r'{{\mathit \tau}^{-}}' : 'tau+',

r'{{\mathit \nu}_{{{{\mathit \ell}}}}}' : 'nu_lepton',
r'{{\mathit \nu}_{{\tau}}}' : 'nu_tau',
r'{{\mathit \nu}_{{e}}}' : 'nu_e',
r'{{\mathit \nu}_{{\mu}}}' : 'nu_mu',

r'{{\mathit \pi}^{+}}' : 'pi+',
r'{{\mathit \pi}^{-}}' : 'pi-',

r'{{\mathit K}^{+}}' : 'K+',
r'{{\mathit K}^{-}}' : 'K-',

r'{{\mathit D}}' : 'D',

r'{{\mathit D}}^{0}}' : 'D0',
r'{{\overline{\mathit D}}^{0}}' : 'anti-D0',

r'{{\mathit D}^{+}}' : 'D+',
r'{{\mathit D}^{-}}' : 'D-',

r'{{\mathit D}^{*}{(2010)}^{+}}' : 'D*(2010)+',
r'{{\mathit D}^{*}{(2010)}^{-}}' : 'D*(2010)-',

r'{{\mathit D}_{{2}}^{*}{(2460)}^{+}}' : 'D_2*(2460)+',
r'{{\mathit D}_{{2}}^{*}{(2460)}^{-}}' : 'D_2*(2460)-',

r'{{\mathit D}^{*0}}' : 'D*0',
r'{{\overline{\mathit D}}^{*0}}' : 'anti-D*0',

r'{{\overline{\mathit D}}^{(*)}}' : 'D*',

r'{{\mathit D}^{*+}}' : 'D*+',
r'{{\mathit D}^{*-}}' : 'D*-',

r'{{\mathit D}_{{0}}^{*}{(2300)}^{+}}' : 'D_0*(2300)+',
r'{{\mathit D}_{{0}}^{*}{(2300)}^{-}}' : 'D_0*(2300)-',

r'{{\mathit \rho}^{+}}' : 'rho+',
r'{{\mathit \rho}^{-}}' : 'rho-',

r"{{\mathit D}_{{1}}^{\,'}{(2430)}^{-}}" : "D_1'(2430)-",
r"{{\mathit D}_{{1}}^{\,'}{(2430)}^{+}}" : "D_1'(2430)+",

r"{{\mathit D}_{{1}}{(2420)}^{-}}" : "D_1(2420)-",
r"{{\mathit D}_{{1}}{(2420)}^{+}}" : "D_1(2420)+",

}

# Add some spaces aferwards for readability
# Probably have some better separator in future

for k, v in particleNames.items():
    particleNames[k] = f'{v} '

particleRegex = re.compile("(%s)" % "|".join(map(re.escape, particleNames.keys())))

def replace_particles(regex, d, text):

    return regex.sub(lambda mo: d[mo.string[mo.start():mo.end()]], text)

# https://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex
def multiple_replace(d, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, d.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: d[mo.string[mo.start():mo.end()]], text)

def getJSExpansions(fileName):

    f = open(fileName, 'r')

    soup = BeautifulSoup(f, 'html.parser')

    # Find JS to open *all* dropdowns

    for link in soup.find_all('a'):
        js = link.get('onclick')
        if js and js[:3] == 'get':
            print(js)

    for link in soup.find_all('script'):
        print(link)

def getRawModes(fileName):

    f = open(fileName, 'r')

    soup = BeautifulSoup(f, 'html.parser')

    for i, link in enumerate(soup.find_all("tr")):

        if not 'gamma' in str(link):
            continue

        padPrev = 0
        parentDecays = []

        for t in link.find_all("td"):
            scripts = t.find_all("script")

            if len(scripts) >= 3 and 'Gamma' in str(scripts[0]):

                # TODO: Compile all of these regexes.

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

                modes = scripts[1:-1]
                modesLatex = []
                for m in modes:
                    latexWrapper = '<script id="MathJax-Element-.*" type="math/tex">(.*)</script>'
                    match = re.search(latexWrapper, str(m))
                    if match:
                        modesLatex.append(match.group(1))

                print('Subdecay : ', parentDecays)

                print('Gamma : ', scripts[0])
                print('Padding : ', pad)
                # print('Contents :', modes)
                print('Contents :', modesLatex)

                # Just do it for the first entry for now,
                # to avoid having to worry about the sub-decays
                if len(modesLatex) > 0:
                  s = replace_particles(particleRegex, particleNames, str(modesLatex[0]))
                  print('Parsed contents : ', s)

                print('BF : ', scripts[-1])
                print('')

        return

        print('')

if __name__ == '__main__':

    getRawModes('testInputs/testPDG.html')
