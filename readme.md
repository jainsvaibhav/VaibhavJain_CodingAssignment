# Censys Project SWE Summer Internship

### Problem Statement
Using the [Censys API](https://search.censys.io/api) and [Python library](https://github.com/censys/censys-python), implement a script that queries the index of the certificate and outputs a CSV of the SHA256 fingerprints and validity start and end dates for all trusted (unexpired) X.509 certificates associated with the censys.io domain. The query for this is parsed.names:
censys.io and tags: trusted.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install censys using "requirements.txt" file.

```bash
pip install -r requirements.txt
```

## Run app.py

### Credentials
Find your credentials on the [Account page](https://search.censys.io/account/api).

```
CENSYS_API_ID = YOUR CENSYS_API_ID
CENSYS_API_SECRET = YOUR CENSYS_API_SECRET
```



#### Run
```bash
python app.py CENSYS_API_ID CENSYS_API_SECRET
```

## Output/Result File

```bash
FILENAME = "out.csv"
```
