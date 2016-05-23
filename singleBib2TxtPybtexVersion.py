from pybtex.database import parse_file
import os
import io
import re
import argparse

__author__ = "Richard Schwarzl (rschwarz@zedat.fu-berlin.de)"

KEYS = "ID", "title", "author", "year", "month", "partOf", "source"


class Bib2Str:
    def __init__(self, bib_string):
        self.bib_str = bib_string
        self.bib_str_split = ""
        self.bib_type = ""
        self.dictionary = {}
        self.strip_at_and_end()
        self.get_type()
        self.split_bib_str()
    def strip_at_and_end(self):
        if self.bib_str == "":
            print("self.bib_str is empty. check your bib entry.")
        else:
            self.bib_str = self.bib_str[1:]
            if self.bib_str[-4:] == "\"\n}\n":
                self.bib_str = self.bib_str[:-4]
            elif self.bib_str[-3:] == "\"\n}":
                self.bib_str = self.bib_str[:-4]
            else:
                print("end of bib string could not be subtracted due to unrecognized format. conversion will not work.")

    def get_type(self):
        self.bib_type = (re.split("{", self.bib_str)[0]).lower()

    def split_bib_str(self):
        self.bib_str = self.bib_str[len(self.bib_type) + 1:]
        self.bib_str_split = re.split("\",\n    | = \"|,\n    ", self.bib_str)
        self.bib_str_split.insert(0, "ID")
        keys = self.bib_str_split[::2]
        values = self.bib_str_split[1::2]
        dictionary = dict(list(zip(keys, values)))
        if "pages" in list(dictionary.keys()):
            dictionary["pages"] = re.sub("--", "-", dictionary["pages"])
        self.dictionary = dictionary

    def write_txt(self):
        if not self.dictionary:
            print("Nothing to write. Load a bib file using read_bib() before you use this module.")
        else:
            try:
                os.remove((self.dictionary["ID"]).lower() + ".txt")
            except IOError:
                pass
            if len(self.dictionary.keys()) < 7:
                raise AttributeError("There is at least one required argument missing {}. Available keys: {}".format(KEYS, self.dictionary.keys()))
            else:
                with io.open((self.dictionary["ID"]).lower() + ".txt", "w", encoding='utf8') as bib2txt_file:
                    bib2txt_file.write(
                        "name\ttitle\tbody\tfuDCcreator\tfuDCdateYear\tfuDCdateMonth\tfuDCrelationPartOf\tfuDCsource\n")
                    for i in ["ID", "title", "body", "author", "year", "month", "partOf", "source"]:
                        if i == "body":
                            try:
                                bib2txt_file.write(
                                    self.dictionary["abstract"] + "\t")
                            except:
                                bib2txt_file.write("\t")
                                print("no abstract in bibtex. body was set to "".")
                        elif i == "month":
                            monthnr = ["jan", "feb", "mar", "apr", "may", "jun", "jul",
                                       "aug", "sep", "oct", "nov", "dec"].index(self.dictionary[i]) + 1
                            if monthnr < 10:
                                bib2txt_file.write(str(0) + str(monthnr) + "\t")
                            else:
                                bib2txt_file.write(str(monthnr) + "\t")
                        elif i == "partOf":
                            try:
                                bib2txt_file.write(self.dictionary["journal"] + " " + self.dictionary["volume"] + ", " + self.dictionary["pages"] + "\t")
                            except:
                                try:
                                    bib2txt_file.write(self.dictionary["booktitle"] + ", " + self.dictionary["pages"] + "\t")
                                except:
                                    print("self.dictionary[", i, "] ", "returned error")
                        elif i == "source":
                            try:
                                bib2txt_file.write("http://dx.doi.org/" + self.dictionary["doi"])
                            except:
                                try:
                                    bib2txt_file.write(self.dictionary["url"])
                                except:
                                    print("self.dictionary[", i, "] ", "returned error")
                        else:
                            try:
                                bib2txt_file.write(self.dictionary[i] + "\t")
                            except:
                                print("self.dictionary[", i, "] ", "returned error")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('file', metavar='file', help='Path to bibtex file.')
    args = ap.parse_args()
    bib_data = parse_file(args.file)
    bib_string = bib_data.to_string("bibtex")
    single_bib2str = Bib2Str(bib_string)
    single_bib2str.write_txt()
    print("utf-8 string has been written to ", single_bib2str.dictionary["ID"] + ".txt")
