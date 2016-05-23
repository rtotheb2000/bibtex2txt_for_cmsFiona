# bibtex2txt_for_cmsFiona

## Description

This python script converts a single bibtex file to a tab stop seperated text file in utf-8 format using pybtex:

**pybtex** (https://pypi.python.org/pypi/pybtex)

To install all dependencies type `pip install -r requirements.txt`

## How to use

Run the script from terminal by switching to the directory, you saved the script, in and type:

python singleBib2TxtPybtexVersion.py

The script will ask you for the file path of the bibtex file, you want to convert. If you have put the bibtex file into the same directory as this script, you can simply type in the file name (e.g. sample.bib). Please make sure your bibtex file only includes one entry. Multiple entries are not yet supported. This script also only supports entries that have the following attributes:

"title", "abstract" (optional), "author", "year", "month", "journal", "volume", "pages", "doi"(or "source")

which is in principle is the type article.

The generated text file can be used to import a dublin core entry (https://en.wikipedia.org/wiki/Dublin_Core) in the content management system of the Freie Universitaet Berlin (Fiona).
In Fiona create a directory using the template "Publikationsliste (Dublin Core)" or use an existing "Publikationsliste (Dublin Core)" directory.
Click on this directory and then use Datei -> CSV-Datei importieren und konvertieren.
Choose utf-8 as encoding and select the text file you have created using this python script.
