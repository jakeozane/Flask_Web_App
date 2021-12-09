# Install

```sh
sudo apt-get install python-dev python3-dev
sudo apt-get install libmysqlclient-dev
pip3 install --user -r requirements.txt
```

# Run

```
python3 server.py
```
## Outdated / Backup

```
export FLASK_APP=server.py; flask run --host 0.0.0.0 --port 4096
```
# Compile PDF with `pandoc`

```bash
filename='portfolio.md'
pandoc "$filename" -o "${filename%%.*}.pdf" -V geometry:margin=1in --highlight=kate
```
