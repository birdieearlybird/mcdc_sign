from bottle import route, run
import requests
import os
import pathlib
import re
import xml.dom.minidom
from bs4 import BeautifulSoup

etherscan_mcdc_link = 'https://etherscan.io/token/0x8937041c8c52a78c25aa54051f6a9dada23d42a2?a=0x76d629ebad7fdf703ed5923f41f20c472e8f23e3'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def alter_svg_text(signText, signOption=0):
    script_dir = pathlib.Path(__file__).parent.absolute()

    svg_file = os.path.join(script_dir, "mcdc_sign.svg")
    svg_write = os.path.join(script_dir, "mcdc_hodlers.svg")

    svg_data = xml.dom.minidom.parse(svg_file)
    name = svg_data.getElementsByTagName('tspan')
    if signOption == 0:
        for t in name:
            if (t.attributes['id'].value=='tspan2242'):
                t.childNodes[0].nodeValue = signText
    f = open(svg_write, 'w')
    f.write(svg_data.toprettyxml())
    f.close()


@route('/sign_hodlers')
def gen_sign_hodlers():
    r = requests.get(etherscan_mcdc_link, headers=headers)
    print(r)
    if r.status_code == 200:
        parsed_html = BeautifulSoup(r.content, 'html.parser')
        hodlers = re.sub("\D", "", parsed_html.body.find('div', attrs={'id':'ContentPlaceHolder1_tr_tokenHolders'}).text)
        print(hodlers)

        return alter_svg_text(hodlers)

#run(host='localhost', port8080, debug=True)
gen_sign_hodlers()
