# xmlToRenumar
## Presentation
The scripts in this repository:
* convert an XML-TEI file into a set of XML-formatted paragraphs adapter for [the Renumar database](http://renumar.univ-tours.fr/) (script `simplifyXmlForRenumar.py`)
* automatically upload the paragraphs as well as some metadata as new documents into the back-office form of Renumar (script `fillOutRenumarForm.py`)

You can also visit the page https://philippegambette.github.io/xmlToRenumar to upload an XML-TEI file, where placeName tags have a ref attribute containing a Geonames id (`geo:...`) and where persName tags have a ref attribute containing either an Idref id (`idref:...`), a VIAF id (`viaf:...`) or a Wikidata id (`wdt:...`) to automatically create a map of those locations and a gallery of these persons (when they are associated with an image in Wikidata).

## Credits
Coded by Philippe Gambette, with the help of Nicole Dufournaud and the documentation and advice by David Rivaud.

## Version history
* 2022-11-25: wd-geocoder: map + gallery from persName and placeName tags
* 2022-11-24: first properly commented version