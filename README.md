# zanikle_obce_cz
The graphical interface for database of czech forgotten places http://www.zanikleobce.cz/index.php?menu=93. It might be found useful for urbexers and hikers.

### Execution
```
./gui_plaground
```
### Required packages:
- PyQt5
- sqlite3
- geopy
- folium
- bs4 (beautiful soup)
- overpy

### Current functionality:
- Fill in coordinates of place and radius, if want to search abandoned places in radius around that place. Click Draw map by coordinates
- Fill in Town name, if want to search abandoned places in given town
- Map can be saved as html or png
- The web page is being updated, so database update should be run sometimes. 
