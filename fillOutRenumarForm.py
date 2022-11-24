#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

import re, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from xml.dom import minidom
import operator

# Please insert you login and password here:
renumarLogin = "foo"
renumarPassword = "bar"

months = [
"1540-09",
"1540-10",
"1540-11",
"1540-12",
"1541-01",
"1541-02",
"1541-03",
"1541-04",
"1541-05",
"1541-06",
"1541-07",
"1541-08",
"1541-09",
"1541-10",
"1541-11",
"1541-12",
"1542-01",
"1542-02",
"1542-03",
"1542-04",
"1542-05",
"1542-06",
"1542-07",
"1542-08",
"1542-09",
"1542-10",
"1542-11",
"1542-12",
"1543-01",
"1543-02",
"1543-03",
"1543-04",
"1543-05",
"1543-06",
"1543-07",
"1543-08",
"1543-09",
"1543-10",
"1543-11",
"1543-12",
"1544-01",
"1544-02",
"1544-03",
"1544-03",
"1549-04",
"1549-05",
"1549-06",
"1549-07",
"1549-08"
]

monthsInFrench = [
"de septembre 1540",
"d'octobre 1540",
"de novembre 1540",
"de décembre 1540",
"de janvier 1541",
"de février 1541",
"de mars 1541",
"d'avril 1541",
"de mai 1541",
"de juin 1541",
"de juillet 1541",
"d'aout 1541",
"de septembre 1541",
"d'octobre 1541",
"de novembre 1541",
"de décembre 1541",
"de janvier 1542",
"de février 1542",
"de mars 1542",
"d'avril 1542",
"de mai 1542",
"de juin 1542",
"de juillet 1542",
"d'aout 1542",
"de septembre 1542",
"d'octobre 1542",
"de novembre 1542",
"de décembre 1542",
"de janvier 1543",
"de février 1543",
"de mars 1543",
"d'avril 1543",
"de mai 1543",
"de juin 1543",
"de juillet 1543",
"d'aout 1543",
"de septembre 1543",
"d'octobre 1543",
"de novembre 1543",
"de décembre 1543",
"de janvier 1544",
"de février 1544",
"de mars 1544",
"de mars 1544",
"d'avril 1549",
"de mai 1549",
"de juin 1549",
"de juillet 1549",
"d'aout 1549"
]

paragraphs = [
]

inputText = open("Marguerite-frotte-Dufournaud.xml.renumar.txt", "r", encoding="utf-8")
currentParagraph = ""
numParagraph = -1

# Prepare the documents to add: they are separated by the ¤ character
for line in inputText:
   res = re.search("^(.*)¤(.*)$", line)
   if res:
      if numParagraph >= 0:
         currentParagraph += res.group(1)
         paragraphs.append(currentParagraph)
      currentParagraph = res.group(2)
      numParagraph += 1
   currentParagraph += line
inputText.close()

paragraphs.append(currentParagraph)
print(paragraphs)
print(len(paragraphs))
print(len(months))


driver = webdriver.Firefox()

# Take 15 seconds to wait until the login form is loaded
time.sleep(15)
driver.get("http://form-tei.irht.cnrs.fr")
driver.execute_script("$('#login').val('" + renumarLogin + "');")
driver.execute_script("$('#mdp').val('" + renumarPassword + "');")
driver.find_element_by_css_selector('input[type="submit"]').click()

numParagraph = 0
for paragraph in paragraphs:
    #Start a new form: wait until the page is loaded
    time.sleep(5)
    time.sleep(5)
    time.sleep(5)
    time.sleep(5)
    print("Click on 'New'")
    driver.find_element_by_css_selector('input[value="Nouveau"]').click()
    time.sleep(10)
    date_norm = months[numParagraph]
    print(date_norm)
    
    driver.find_element_by_css_selector('input[name="transcriptionChk"]').click()
    driver.find_element_by_css_selector('input[name="analyseChk"]').click()
    name="analyseChk"
    # n1.44 -> n1.45 passage de 1543 à 1548
    # Prepare data to fill out the form
    data = {
      "#typeActe": "Compte",
      "#formeActe": "Registre particulier de comptes",
      "#dateMinute_1": monthsInFrench[numParagraph].replace("d'","").replace("de ",""),
      "#dateMinuteNormalisee_1": date_norm + "-01",
      "#nomPrenomNotaire_1": "Marguerite de Navarre",
      "#villeNotaire": "", 
      "#statutEdition_1": "Première édition",
      "#commentaireEdition_1": "Hector de La Ferrière-Percy Aubry, Marguerite d’Angoulême (sœur de Francois I.), son livre de dépenses (1540-1549), étude sur ses dernières années, 1862",
      "#prenomResponsableRevision_1": "Nicole",
      "#nomResponsableRevision_1": "Dufournaud",
      "#paragAnalyse": "Version mise au propre du registre des comptes par Jehan de Frotté, « contrerolleur general et secrectaire des finances des Roy et Royne de Navarre », pour le mois " + monthsInFrench[numParagraph] + ".",
      "#paragTranscription": paragraphs[numParagraph],
      "#ville": "-",
      "#institution": "Collection particulière", 
      "#cote": "XCollPriv_Frotte_0001",
      
    }
    print(data);
    # Fill in the text area fields of the form
    driver.execute_script('$("#paragAnalyse").data("CodeMirrorInstance").toTextArea()')
    driver.execute_script('$("#paragTranscription").data("CodeMirrorInstance").toTextArea()')
    # fill in the other fields of the form
    for d in data:
      print(d + "->" + data[d])
      print("$('"+ d +"').val('" + data[d].replace("'","’") + "');")
      driver.execute_script("$('"+ d +"').val('" + data[d].replace("\n","").replace("\r","").replace("'","’") + "');")
    # Save the current form and wait until the form is saved (60 seconds)
    driver.execute_script("submitEnreg('manuscrit')")
    time.sleep(60)
    
    # Go back to the home page of the Renumar backoffice and wait until it is loaded (20 seconds)
    driver.execute_script("if (!window.verifModifsAvantListe || verifModifsAvantListe()) goTo('/manuscrit/liste')")
    time.sleep(20)
    numParagraph += 1