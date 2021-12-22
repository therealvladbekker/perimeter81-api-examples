Here is a utility which will allow you to import groups from a properly formatted XLS (Excel) file. You'll need two columns, one with the exact spelling (case sentsitive) of the group and another with it's description. It is written in python 3 and you can run as like so:

Usage:
```
$ python3 createGroups.py --help
usage: createGroups.py [-h] --apikey APIKEY [--file FILE]

optional arguments:
  -h, --help            show this help message and exit
  --apikey APIKEY, -A APIKEY
                        argument takes in the API key from web portal
  --file FILE, -F FILE  argument takes in an excel format file with groups/descriptions
```

Requirements:
