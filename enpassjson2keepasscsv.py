import json
import sys
import csv
import os.path

class PasswordItem:
    def __init__(self):
        super().__init__()
        self.group = ''
        self.title = ''
        self.username = ''
        self.password = ''
        self.url = ''
        self.notes = ''

def main():
    destinationFileName = 'keepass.csv'
    if os.path.exists(destinationFileName):
        log(destinationFileName+' already exists, therefore the export can not be continued.')
        return

    if len(sys.argv)<2:
        print("Please specify a JSON to be converted.")
        return

    fileName = sys.argv[1]
    if not os.path.exists(fileName):
        log('The import file '+fileName+' does not exist.')
        return

    with open(fileName) as f:
        enpassJson = json.load(f)

        folderDict = {}
        for folderItem in enpassJson['folders']:
            folderDict[folderItem['uuid']] = folderItem['title']

        knownFieldTypes = ['username', 'password', 'url']

        passwordItems = []
        for item in enpassJson['items']:
            passwordItem = PasswordItem()
            passwordItem.title = item['title']

            # User the folder name as group:
            if 'folders' in item:
                for folderId in item['folders']:
                    passwordItem.group = folderDict[folderId]
                    break

            # In case there is no folder we use the category as group:
            if 'category' in item and not passwordItem.group:
                passwordItem.group = item['category']

            if 'note' in item:
                passwordItem.notes = item['note']

            if 'fields' in item:
                for field in item['fields']:
                    fieldType = field['type']
                    fieldValue = field['value']
    
                    if fieldValue:
                        # Add all unsupported fields to the notes field:
                        if 'label' in field and fieldType not in knownFieldTypes:
                            if (passwordItem.notes):
                                passwordItem.notes += '\n'
                            passwordItem.notes += field['label']+': '+fieldValue
                        # Add the normal fields to the item:
                        if fieldType=='password' and not passwordItem.password:
                            passwordItem.password = fieldValue
                        elif fieldType=='username' and not passwordItem.username:
                            passwordItem.username = fieldValue
                        elif fieldType=='url' and not passwordItem.url:
                            passwordItem.url = fieldValue

            passwordItems.append(passwordItem)
        
        with open('keepass.csv', 'x', newline='') as exportCSV:
            csvWriter = csv.writer(exportCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            for passwordItem in passwordItems:
                csvWriter.writerow([passwordItem.group, passwordItem.title, passwordItem.username, passwordItem.password, passwordItem.url, passwordItem.notes])
            log('Added '+str(len(passwordItems))+' items to keepass.csv.')

def log(logString: str):
    print(logString)

main()
