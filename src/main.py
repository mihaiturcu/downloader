import requests
import re
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest



def FetchPDF(url):
    content = requests.get(url)
    if content.status_code == 200:
        print("Success, moving forward")
        #print(content.text)
        for line in content.text.splitlines():
            #print(line)
            if ".pdf" in line:
                extractedurl = re.findall("src.*", str(line))
                #extractedurl = extractedurl[0].split('"')
                url = extractedurl[0].split('"')
                url = url[1].split("file=")
                url = url[1].split("&pgnr")
                url = url[0].split("../../")
                print(url[1])
                finalurl = "https://bcucluj.ro/" + url[1]
                print(finalurl)
                return(str(finalurl))
                #print(url[1])

#https://www.bcucluj.ro/synfilebibdigit/Scan2020/Istorie%20si%20Filosofie/Studii%20de%20securitate/Examen%20licenta/Buzan_Barry-Securitatea_nou_cadru-2011.pdf
#https://www.bcucluj.ro/synfilebibdigit/Scan2020/Istorie si Filosofie/Studii de securitate/Examen licenta/Buzan_Barry-Securitatea_nou_cadru-2011.pdf

#FetchPDF("https://www.bcucluj.ro/public-view/vpdf.php?htsbt=fgdf6fgsdGNFJE|Istorie%20si%20Filosofie/Studii%20de%20securitate/Examen%20licenta/Buzan_Barry-Securitatea_nou_cadru-2011.pdf")



class UI(GridLayout):
    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="url: "))
        self.url = TextInput(multiline=False)
        self.inside.add_widget(self.url)

        self.inside.add_widget(Label(text="download url: "))
        self.downloadurl = TextInput(multiline=False)
        self.inside.add_widget(self.downloadurl)

        self.add_widget(self.inside)

        self.submit = Button(text="Go", font_size=40)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

    def pressed(self, instance):
        url = self.url.text
        downloadurl = FetchPDF(url)
        print("\n" + str(downloadurl))
        print("url:", url)
        self.downloadurl.text = downloadurl


class Downloader(App):
    def build(self):
        return UI()


if __name__ == '__main__':
    Downloader().run()
