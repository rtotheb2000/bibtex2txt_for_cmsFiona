from pybtex.database import parse_file
import io
import re

root = tk.Tk()
root.withdraw()
file_path = raw_input("type in bibtex file path (if the bibtex file is in the same directory as this python script just type in the bibtex file name): ")

bib_data = parse_file(file_path)

bib_string = bib_data.to_string("bibtex")

class bib2str:

    def __init__(self, bib_string):
        self.bib_str = bib_string
        self.bib_str_split = ""
        self.bib_type = ""
        self.dictionary = []
        self.description = "This is a publication entry for the homepage. The idea is to convert a bib file to a txt output that can be directly imported into the content management system used by the Freie Universitaet Berlin."
        self.author = "Richard Schwarzl (2016, rschwarz@zedat.fu-berlin.de)"
        self.strip_at_and_end()
        self.get_type()
        self.split_bib_str()
        
    def strip_at_and_end(self):
        if self.bib_str == "":
            print "self.bib_str is empty. check your bib entry."
        else:
            self.bib_str = self.bib_str[1:]
            if self.bib_str[-4:] == "\"\n}\n":
                self.bib_str = self.bib_str[:-4]
            elif self.bib_str[-3:] == "\"\n}":
                self.bib_str = self.bib_str[:-4]
            else:
                print "end of bib string could not be subtracted due to unrecognized format. conversion will not work."

    def get_type(self):
        self.bib_type = (re.split("{",self.bib_str)[0]).lower()
    
    def split_bib_str(self):
        self.bib_str = self.bib_str[len(self.bib_type)+1:]
        self.bib_str_split = re.split("\",\n    | = \"|,\n    ",self.bib_str)
        self.bib_str_split.insert(0,u"ID")
        keys = self.bib_str_split[::2]
        values = self.bib_str_split[1::2]
        dictionary = dict(zip(keys, values))
        if "pages" in dictionary.keys():
            dictionary["pages"]=re.sub("--","-",dictionary["pages"])
        self.dictionary = dictionary
    
    def write_txt(self):
        if self.dictionary=="":
            print "Nothing to write. Load a bib file using read_bib() before you use this module."
        else:
            try:
                os.remove((self.dictionary["ID"]).lower()+".txt")
            except:
                pass
            if len(self.dictionary.keys())<7:
                print "There is at least one required argument missing (ID, title, author, year, month, partOf, source)"
            else:
                with io.open((self.dictionary["ID"]).lower()+".txt","w",encoding='utf8') as bib2txt_file:
                    bib2txt_file.write(u"name\ttitle\tbody\tfuDCcreator\tfuDCdateYear\tfuDCdateMonth\tfuDCrelationPartOf\tfuDCsource\n")
                    for i in ["ID","title","body","author","year","month","partOf","source"]:
                        if i == "body":
                            try:
                                bib2txt_file.write(self.dictionary["abstract"]+u"\t")
                            except:
                                bib2txt_file.write(u"\t")
                                print "no abstract in bibtex. body was set to ""."
                        elif i == "month":
                            monthnr=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"].index(self.dictionary[i])+1
                            if monthnr<10:
                                bib2txt_file.write(str(0).decode("utf-8")+str(monthnr).decode("utf-8")+u"\t")
                            else:
                                bib2txt_file.write(str(monthnr).decode("utf-8")+u"\t")
                        elif i=="partOf":
                            try:
                                bib2txt_file.write(self.dictionary["journal"]+u" "+self.dictionary["volume"]+u", "+self.dictionary["pages"]+u"\t")
                            except:
                                try:
                                    bib2txt_file.write(self.dictionary["booktitle"]+u", "+self.dictionary["pages"]+u"\t")
                                except:
                                    print "self.dictionary[",i,"] ","returned error"
                        elif i=="source":
                            try:
                                bib2txt_file.write(u"http://dx.doi.org/"+self.dictionary["doi"])
                            except:
                                try:
                                    bib2txt_file.write(self.dictionary["url"])
                                except:
                                    print "self.dictionary[",i,"] ","returned error"
                        else:
                            try:
                                bib2txt_file.write(self.dictionary[i]+u"\t")
                            except:
                                print "self.dictionary[",i,"] ","returned error"


single_bib2str=bib2str(bib_string)
single_bib2str.write_txt()
print "utf-8 string has been written to ", single_bib2str.dictionary["ID"]+".txt"



