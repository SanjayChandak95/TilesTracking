import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen,ScreenManager
import xml.etree.ElementTree as ET
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from copy import deepcopy
kivy.require('1.11.1')
#three Window for descriptions
class FirstDescription(Screen):
    pass

class AddTiles(Screen):
    tileName = ObjectProperty(None)
    quantity = ObjectProperty(None)

    def addIt(self):
        addQuantity = int(self.quantity.text)
        msg = ''
        tree = ET.parse('MTS_Tiles_Stock.xml')
        root = tree.getroot()
        if addQuantity <= 0:
            msg = "Can't add negative"
        elif self.tileName.text == "TEST":
            msg = "You don't have access to add TEST"
        else:
            tileDetail = root.find("./tile/[name = '" + self.tileName.text + "' ]")
            if tileDetail:
                stockQuantity = int(tileDetail.find('./quantity').text)
                newQuantity = stockQuantity + addQuantity

                tileDetail.find('./quantity').text = str(newQuantity)
                tree.write('MTS_Tiles_Stock.xml')
                msg = "Successfully Update"
            else:
                msg = 'Create New Tiles'
                tileDetail = root.find("./tile/[name = 'TEST' ]")
                tileDetail = deepcopy(tileDetail)
                tileDetail.find('./name').text = self.tileName.text
                tileDetail.find('./quantity').text = self.quantity.text
                root.append(tileDetail)
                tree.write('MTS_Tiles_Stock.xml')
        self.tileName.text = self.quantity.text = ''
        popup = Popup(title='Remove Tiles',
                      content=Label(text=msg),
                      size_hint=(None, None), size=(400, 400))
        popup.open()


class RemoveTiles(Screen):
    tileName = ObjectProperty(None)
    quantity = ObjectProperty(None)
    def removeIt(self):
        msg = ''
        if self.tileName.text == 'TEST':
            msg = "You don't have access to add TEST"
        else:
            removeQuantity = int(self.quantity.text)
            tree = ET.parse('MTS_Tiles_Stock.xml')
            root = tree.getroot()
            tileDetail = root.find("./tile/[name = '"+self.tileName.text+"' ]")

            if tileDetail:
                stockQuantity = int(tileDetail.find('./quantity').text)
                if stockQuantity < removeQuantity:
                    msg = 'Stock have only {} quantity!\n Hence no update'.format(stockQuantity)
                else:
                    newQuantity = stockQuantity-removeQuantity
                    if newQuantity == 0:
                        root.remove(tileDetail)
                    else:
                        tileDetail.find('./quantity').text = str(newQuantity)
                    tree.write('MTS_Tiles_Stock.xml')
                    msg = "Successfully Update"
            else:
                msg  = 'No Tiles With this Name'
        self.tileName.text = self.quantity.text = ''
        popup = Popup(title='Remove Tiles',
                      content=Label(text=msg),
                      size_hint=(None, None), size=(400, 400))
        popup.open()


class DisplayTiles(Screen):
    tileName = ObjectProperty(None)
    stockresult = ObjectProperty(None)
    result = ''
    def searchResult(self):
        tree = ET.parse('MTS_Tiles_Stock.xml')
        root = tree.getroot()
        allList = root.findall('./tile')
        if self.tileName.text != '' and self.tileName.text != None:
            allList = root.findall("./tile/[name = '"+self.tileName.text+"' ]")
        temp =[]
        for x in allList:
             if x.find('./name').text != 'TEST':
                temp.append(str(x.find('./name').text+ "-->" +x.find('./quantity').text))
        self.result = '\n'.join(temp)
        self.stockresult.text = self.result



class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MTSTilesStock(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MTSTilesStock().run()