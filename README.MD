## Usage:
```python
from scraper import extractAllProvision, cleanSubProvisions

url = 'path/to/the/file.html'
result = cleanSubProvisions(extractAllProvision(url))
```

## Files:
- scraper.py
  The file contains all functions

- test.py
  Test file that contains test codes

- *.xlsx
  Test Results

## Requirments:
- lxml
- BeautifulSoup
- urllib
