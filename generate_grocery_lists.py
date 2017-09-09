# encoding= utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import xlrd
import json
import requests
from googletrans import Translator

class GroceryList:
    def __init__(self, filename, language_code="en"):
        self.filename = filename
        self.language_code = language_code

    def generate(self):
        # DOWNLOAD THE SPREEDSHEET

        url = "http://www.grocerylists.org/wp-content/uploads/2013/01/grocerylistsDOTorg_Spreadsheet_v1_1.xls"
        response = requests.request("GET", url)
        with open("grocerylistsDOTorg_Spreadsheet_v1_1.xls", "w") as f:
            f.write(response.content)

        # PARSE THE SPREEDSHEET -> .TXT FILE
        items = []

        ITEM_LOC_START = 3
        ITEM_LOC_END = 12

        categories = ["FOODSTUFFS", "HOUSEHOLD"]
        subcategories = ["Fresh vegetables", "Condiments / Sauces", "Dairy", "Baked goods", "Personal care", "Cleaning products", "Fresh fruits", "Various groceries", "Cheese", "Baking", "Medicine", "Office supplies", "Refrigerated items", "Canned foods", "Seafood", "Themed meals", "Kitchen", "Other stuff",
                              "Frozen", "Spices & herbs", "Beverages", "Baby stuff", "Other", "Pets"]

        try:
            book = xlrd.open_workbook("grocerylistsDOTorg_Spreadsheet_v1_1.xls")
            sh = book.sheet_by_index(0)
            for rx in range(ITEM_LOC_START, sh.nrows - ITEM_LOC_END):
                for cell in sh.row(rx):
                    item = cell.value.replace("·", "").strip()
                    if bool(item):
                        if (item not in categories):
                            if (item not in subcategories):
                                items.append(item)

            # TRANSLATE TO SET LOCALE LANGUAGE.
            if self.language_code != "en":
                translator = Translator()
                items = translator.translate("\n".join(items), dest=self.language_code).text.split("\n")


            items = sorted(items)

            # WRITE OUT TO FILE.
            with open(self.filename, "wb+") as f:
                for i in xrange(len(items)):
                    f.write(items[i].capitalize())
                    if i != len(items)-1:
                        f.write("\n")

        except:
            print "Unexpected error occurred"
            raise

languages = ["en", "da", "sv", "no"]
for language in languages:
    GroceryList(filename="Shallow Grocery Lists/%s.txt" % language, language_code=language).generate()
