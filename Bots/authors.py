import requests
from bs4 import BeautifulSoup
import json
from xml.etree import ElementTree as ET
import pandas as pd
import numpy as np
import time
import timeit
from random import *

from pathlib import Path
import os
import sys

import sqlite3
import contextlib

from parserXml import parsear
import re

print('Starting...')

cont = 1
_pause = 0
api_count = 0

api = 	[]

# open connection with SQLite
file = 'autores.db'
conn = sqlite3.connect(file)
c = conn.cursor()

d_total = c.execute("SELECT count(*) FROM authors WHERE sent=0")
total = d_total.fetchall()
print('Records:', total)

cursor = conn.cursor()
data = cursor.execute("SELECT * FROM authors WHERE sent=0")
data = data.fetchall()

for row in data:
	# requisição ao servidor da Elsevier via API
	resp = requests.get(
		"http://api.elsevier.com/content/author?author_id="+ str(row[0]) + "&view=ENHANCED", 
   						headers={	'Accept':'application/xml', 
   									'X-ELS-APIKey': api[api_count]
   								}
   		)
	# salva em arquivo os dados no formato XML
	with open(str(row[0])+".xml", 'wb') as xml:
		xml.write(resp.text.encode('utf-8'))

	file = open(str(row[0]) + '.xml', encoding="utf8")
	page = file.read()
	xmlTree = BeautifulSoup(page, 'xml')

	contador = 0 
	for coredata in xmlTree.findAll('error-response'):
		contador += 1
		print(coredata.text)

	for coredata in xmlTree.findAll('title'):
		if (re.match('404 - Visualização', coredata.text)) != None:
			contador += 1
			print(coredata.text)

	file.close()
	if contador > 0:
		break

	# save data to status in database
	cursor.execute("UPDATE authors SET sent = 1 WHERE author_id = " + str(row[0]))
	conn.commit()

	#faz o parser e grava no sqlite
	parsear(xmlTree, str(row[0]))
	print('Parser:', str(row[0]).zfill(10), str(api_count).zfill(5), api[api_count])

	source = os.path.dirname(os.path.realpath(str(row[0]) + '.xml')) + '\\' + row[0]+'.xml'
	try:
		destination = os.path.dirname(os.path.realpath(str(row[0]) + '.xml')) + '\\data\\' + str(row[0]) + '.xml'
		os.rename(source, destination)
	except:
		print('Record fail in "data"')
		destination = os.path.dirname(os.path.realpath(str(row[0]) + '.xml')) + '\\' + str(row[0]) + '.xml'
		os.rename(source, destination)


	cont += 1
	_pause += 1
	api_count += 1

	if _pause > 100:
		# pause to simulate a human
		print("\n.... pause...\n")
		time.sleep(uniform(1,5))
		_pause = 0

	if api_count > (len(api)-1):
		api_count = 0

# close SQLite connection
conn.close()
