# -*- coding: utf-8 -*-
import csv, glob, os, re, requests, sys, time
from xml.dom import minidom

# Get the current folder
folder = os.path.abspath(os.path.dirname(sys.argv[0]))

# Open the input file
file = "Marguerite-frotte.xml"
file = "XCollPriv_Frotte_0001.xml"
outputFile = open("Marguerite-frotte-Dufournaud.xml.renumar.txt", "w", encoding="utf-8")

num = 0
monthFound = False
    
# as soon as the starting node is found, extract the text, 
# as well as some kept tags (possibly transformed to take into account the constraints of Renumar) 
# inside a node of the XML file, except in the forbidden tags,
# knowing the parent tag and the fact that we are currently keeping the text content 
# if the starting node has been found) or not.
def displayNodeText(node, forbiddenTags, keptTags, parentTag, savingContent, startingNode):
   global num, monthFound
   num += 1
   if node.nodeName == "fw":
      print("!")
   if node.nodeName == startingNode:
      savingContent = True;
   if node.childNodes.length == 0:
      # The current node is a leaf
      if node.nodeName == "lb":
         data = "<br/>"
      else :
         # Get the data inside the node if there is any
         data = ""
         # Ignore data inside comment tags
         if node.nodeName != "#comment":
            try:
               data = node.data
            except:
               pass
      # Return the content of the node if it needs to be exported
      if savingContent:
         return data
      else :
         return ""
   else:
      text = ""
      for child in node.childNodes:
         if child.nodeName not in forbiddenTags:
            # Keep all attributes
            tagAttributes = {}
            try:
               tagAttributes = dict(child.attributes.items())
            except:
               pass
            # Treat the node if its tag is 
            if child.nodeName in keptTags:
               openingTag = "<" + child.nodeName 
               for attribute in tagAttributes:
                  # Convert the sup attribute into an exp attribute
                  if attribute == "rend" and tagAttributes[attribute] == "sup":
                     openingTag += ' rend="exp"'
                  else:
                     openingTag += " " + attribute + "=" + '"' + tagAttributes[attribute] + '"'
               text += openingTag + ">" + displayNodeText(child, forbiddenTags, keptTags, node.nodeName, savingContent, startingNode) + "</" + child.nodeName + ">"
            else:
               # Special cases with the date tag
               if child.nodeName == "date":
                  if not(monthFound):
                     print(tagAttributes["when"])
                  monthFound = True
               # Special cases with some tags
               if child.nodeName == "note" or child.nodeName == "label":
                  # Special case with tag note or label: they become margin notes
                  text += '<note place="margin">' + displayNodeText(child, forbiddenTags, keptTags, node.nodeName, savingContent, startingNode) + '<br/></note>'
               elif child.nodeName == "del":
                  # Special case with tag del
                  text += '<hi rend="striped">' + displayNodeText(child, forbiddenTags, keptTags, node.nodeName, savingContent, startingNode) + '</hi>'
               elif child.nodeName == "div" and "type" in tagAttributes and tagAttributes["type"] == "mois" :
                  # Insert a separator, the character ¤, to show that a new month is starting
                  # This will correspond to a new file in Renumar
                  print("New month found!")
                  monthFound = False
                  text += "¤\n\n" + displayNodeText(child, forbiddenTags, keptTags, node.nodeName, savingContent, startingNode)
               else:
                  # Special cases with tag ab, head or titlePart
                  if child.nodeName == "ab" or child.nodeName == "head" or child.nodeName == "titlePart":
                     text += displayNodeText(child, forbiddenTags, keptTags, node.nodeName, savingContent, startingNode) + "<br/><br/>"
                  else:
                     text += displayNodeText(child, forbiddenTags, keptTags, node.nodeName, savingContent, startingNode) 
      return text

# Write the extracted and transformed text at the Renumar format into the output file
outputFile.writelines(displayNodeText(minidom.parse(file),["teiHeader","fw","orig"],["placeName","persName","hi"],"", False, "text").replace("\r\n","\n").replace("\t"," ").replace("\n"," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("<br/>","<br/>\n").replace("</MARGE>","</MARGE>\n").replace("¤¤","\n").replace("\n "," \n").replace("\n "," \n"))
outputFile.close()