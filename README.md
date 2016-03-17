# Download Data
#### Libs
pip install requests pandas optparse    
apt-get install parallel
#### Usage
```bash
python download_csv.py -u username -p password -e "356700..356800MHz" -i "HARP-ACSIS" -c "JCMT"
```    

```bash
./download_raw.sh
```    

# Starlink
#### vim ~/.bashrc, insert two lines below.
```bash
#### Change starlink folder
export STARLINK_DIR=/hcm/Harry/Radio-Astronomy/Software/star-2015B
source $STARLINK_DIR/etc/profile
```
#### Run red2.sh
Usage
```bash
source  red2.sh  datadir mypar
```
Example
```bash
source  red2.sh  hcop  mypar.ini
```
