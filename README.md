# enpassjson2keepasscsv
## Convert an Enpass JSON export to a CSV file readable by KeePass

The CSV files exported by Enpass are not readable by KeePass because as there are different entry types in Enpass the different lines in the CSV have different information. 

Therefore I created a very simple python script that takes a JSON export from Enpass as parameter and creates a file named keepass.csv containing the information from the JSON file. This CSV file can then be imported into KeePass.

To run the script, simpy pass the JSON file as parameter:
```
python3 enpassjson2keepasscsv.py enpass.json
```
This will read the enpass.json and create a new file named keepass.csv in the current directory.

I just tested the import with KeePassXC so I don't know if it works for other versions of KeePass as well.
