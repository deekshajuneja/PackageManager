import os
import json
import argparse
import pandas as pd
from sys import argv

def main(argv):
	bowerPath = []
	parser = argparse.ArgumentParser()
	parser.add_argument("path", help="Path", nargs='*')
	args = parser.parse_args()
	road = ''.join(args.path)
	os.chdir(road)
	bowerPath.append(os.listdir(road+"bower_components"))
	numbowerFiles = len(os.listdir(road+"bower_components"))
	os.system("npm ll --parseable > npm.txt")
	with open("npm.txt") as f:
		content = f.readlines()
		# print(content)
	moduleName = []
	moduleList = []
	pathList = []
	for line in content:
		# print(line)
		moduleName.append(line.split(':'))
	# print (moduleName)
	for module in moduleName:
		# print (module [1])
		if module[1] not in moduleList and module[2] != 'INVALID':
			moduleList.append(module[1])
			pathList.append(module[0])
	# print(pathList)
	# print(moduleList) # NPM package names
	npmlicense = []
	npmlinklist = []
	for path in pathList:
		os.chdir(path)
		with open('package.json') as f:
			data = json.load(f)
			# print (path)
			if 'license' in data:
				if 'type' not in data["license"]:
					gotLicense = (data["license"])
					npmlicense.append(gotLicense)
					# print(gotLicense)
				else:
					gotLicense = (data["license"]["type"])
					npmlicense.append(gotLicense)
					# print(gotLicense)
			elif 'licenses' in data:
				gotLicense = (data["licenses"][0]["type"])
				npmlicense.append(gotLicense)
				# print(gotLicense)
			else:
				gotLicense = ("License Not Found")
				npmlicense.append(gotLicense)
				# print(gotLicense)
			if 'repository' in data:
				gotnpmLink = (data["repository"])
				if 'url' in gotnpmLink:
					npmLink = (gotnpmLink["url"])
					# print(npmLink)
					npmlinklist.append(npmLink)
	# print(npmlinklist)
	finalnpmlink = []
	appendednpmlink = []
	for link in npmlinklist:
		print (link)
		if 'git:' in link.encode('UTF8'):
			templink = (str.replace(link.encode('UTF8'),'git:', 'git+https:'))
			# print(templink)
			appendednpmlink .append(templink)
		else:
			appendednpmlink.append(link)
	# print (appendednpmlink)

	for link in appendednpmlink:
		splitlink = link.split('+')
		print(splitlink[1])


	bowerModule = []
	bowerComponent = []
	licensebower = []
	for i in range(1,numbowerFiles):
		bowerModule.append(bowerPath[0][i])
	# print(bowerModule) #Bower package Names

	for module in bowerModule:
		bowerComponent.append(road+"bower_components/"+module)
	# print(bowerComponent)

	for path in bowerComponent:
		os.chdir(path)
		with open('bower.json') as bf:
			data = json.load(bf)
			# print(path)
			# print data
			if 'license' in data:
				bowerLicense = data["license"]
				licensebower.append(bowerLicense)
				# print(bowerLicense)
			else:
				bowerLicense = ("license not found")
				licensebower.append(bowerLicense)
				# print(bowerLicense)


##### HomeBrew #####
	homebrewname = []
	homebrewlicense = []
	os.chdir(road)
	os.system("brew list > brew.txt")
	with open ('brew.txt') as hbf:
		homebrewdata = hbf.read()
	# print (homebrewdata.split())
	licensehomebrew = "license not found"
	for name in homebrewdata.split():
		homebrewname.append(name)
		homebrewlicense.append(licensehomebrew)


##### pip #####
	pipname = []
	piplicense = []
	os.chdir(road)
	os.system("pip list > pip.txt")
	with open('pip.txt') as pf:
		pipdata = pf.read()
	# print(pipdata)
	licensepip = "license not found"
	for name in pipdata.split("\n"):
		if name != "":
			pipname.append(name)
			piplicense.append(licensepip)
	# print (pipname)

##### Write Excel Sheet #####
	os.chdir(road)
	df = pd.DataFrame({'Name': moduleList+bowerModule+homebrewname+pipname, 'License': npmlicense+licensebower+homebrewlicense+piplicense, 'Where will this package/library be used? (at least for the first use?)': "LIMS"})
	writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
	df.to_excel(writer, sheet_name='packages')
	workbook = writer.book
	worksheet = writer.sheets['packages']
	worksheet.set_column('B:B', 18)
	worksheet.set_column('C:C', 35)
	worksheet.set_column('D:D', 55)
	writer.save()
	os.system("rm %s %s %s" %("npm.txt", "brew.txt", "pip.txt"))

if __name__ == "__main__":
	main(argv)
