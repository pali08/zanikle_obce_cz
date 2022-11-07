# zanikle_obce_cz
The graphical interface for database of czech forgotten places http://www.zanikleobce.cz/index.php?menu=93. It might be found useful for urbexers and hikers.

### Setup environment and run (linux, possibly mac):
Prerequisites: python3 (tested with python3.8), virtualenv (e.g. package python3-venv on ubuntu)
1. Create directory where program will be stored and go to it:\
`
$ mkdir zanikle_obce && cd zanikle_obce
`
2. Get program code:\
`
$ git clone https://github.com/pali08/zanikle_obce_cz.git
`
3. Create virtual environment and activate it:\
`
$ python3 -m virtualenv -p python3.8 ./venv && cd venv && source ./bin/activate
`
4. Install required libraries either by pip:\
`
$ pip install -r zanikle_obce_cz/requirements.txt
`\
or by script:\
`
$ sh ./zanikle_obce_cz/install_requirements.txt.sh
`\
From what I found, the first option installs libraries as global libraries (not good)
### Execution
`
$ ./main.py
`\
Each time terminal is closed, we need to activate environment before execution:\
`
$ cd zanikle_obce/venv && source ./bin/activate
$ cd ../zanikle_obce_cz && ./main.py
`

### Current functionality:
- Fill in coordinates of place and radius, if want to search abandoned places in radius around that place. Click by coordinates
- Fill in town name, if want to search abandoned places in given town. Click by town (only).
- Fill in town and radius, if want to search places in radius around town center point. Click radius around town
- Map can be saved as html or png
- Database can be updated 
  - either fully (slow, but we can be sure, that all data are up to date)
  - or by only adding new places (faster, but if already added place was updated by user after adding, new data will be missing)
