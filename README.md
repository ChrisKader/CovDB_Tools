# CovDB Update Tools

Project inspired by [PvPDB.io](https://github.com/qwazerty/pvpdb.io)

Toolset used to update the CovDB addon database files with the assistance of RaiderIO database files. I am not an expert python developer (this is my first project using it) so any pull requests with improvements or 'best-practice' suggestions are welcome.

## Requirements
- Python 3
- MongoDB
- [Battle.net API keys](https://develop.battle.net/access/)
- RaiderIO Addon DB files
- Time (This can be reduced exponentially with more workers/api keys.)

## Usage

You will want to setup a file named `tokens.py` and structure it similar to the below example.

```python
tokens = {
  'covdb-worker-1': {
    'bnet-name': 'covdb-Worker-1',
    'client_id': 'XXXXXXXXX',
    'client_secret': 'XXXXXXXXX'
  },
}
mongo_url = 'mongodb://SuperRoot:SuperSecure!@localhost:27017/'
```

Execute the below command (taking into account your own worker name(s) added to `tokens.py`) to intialize the MongoDB databse.

`python .\worker-covdb.py init covdb-Worker-1`

Execute the below command to begin updating the initialzed database. You can spawn multiple processes if you have multiple workers in your `tokens.py` file

`python .\worker-covdb.py update covdb-Worker-1`

## Roadmap
- [ ] Improve `worker-covdb.py` file to make updating more efficiently
    - [ ] Use ```If-Modified-Since``` HTTP Headers
        - This reduces the overall cost of API calls against each token as any data not updated since the timestamp provided during the intial request does not count as a call.
    - [ ] Handle worker allocation within the script