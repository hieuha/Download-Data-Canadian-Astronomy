# Download-Data-Canadian-Astronomy
## Libs
pip install requests pandas   
apt-get install parallel
## Usage
```python
    username = ''
    password = ''
    energy_value = '356700..356800MHz'
    main(username, password, energy_value)
```    
1, $python download_csv.py    
2, $chmod +x download_raw.sh    
3, $./download_raw.sh    

# Starlink
## vim ~/.bashrc, insert two lines below.
```bash
# Change starlink folder
export STARLINK_DIR=/hcm/Harry/Radio-Astronomy/Software/star-2015B
source $STARLINK_DIR/etc/profile
```
## Run red2.sh
Usage
```bash
source  red2.sh  datadir mypar
```
Example
```bash
source  red2.sh  hcop  mypar.ini
```
