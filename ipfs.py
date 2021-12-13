import ipfsapi

from logger import log

MESSAGE = 'Hello World'

log("Start")
f = open('file.txt', 'w')
log("File opened")
f.write(MESSAGE)
log("File written")
f.close()
log("File closed")
api = ipfsapi.Client(host='https://ipfs.infura.io', port=5001) #api = ipfsApi.Client(host='http://127.0.0.1', port=5001)
log("Start Upload")
new_file = api.add('file.txt')
log(new_file)
data = api.cat(new_file['Hash'])
log("Done Redownload")
