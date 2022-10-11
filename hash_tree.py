import hashlib
import json

HASHES_FILE = 'hashes.json'

class HashTree():
    def __init__(self, divs):
        self.divs = divs
        try:
            json_string = open(HASHES_FILE, 'r').read()
            dict = json.loads(json_string)
            self.root_hash = dict['root_hash']
            self.hashes = set(dict['hashes'])
            self.no_inital_hashes_file = False
        except:
            self.no_inital_hashes_file = True


    def find_diffs(self):
        if self.no_inital_hashes_file:
            return self.divs
        if _compute_root_hash(self.divs) == self.root_hash:
            return []
        diffs = []
        for div in self.divs:
            div_hash = _compute_hash(div)
            if not div_hash in self.hashes:
                diffs.append(div)        
        return diffs

    def update(self):
        self.hashes = set()
        for div in self.divs:
            self.hashes.add(_compute_hash(div))
        self.root_hash = _compute_root_hash(self.divs)
        json_string = json.dumps({'root_hash': self.root_hash, 'hashes': list(self.hashes)}, indent=4)
        file = open(HASHES_FILE, 'w')
        file.write(json_string)
        file.close()

def _compute_hash(div):
    identifier = div.find("a", class_="internal-link")['href']
    hash = hashlib.sha256(identifier.encode('ascii')).hexdigest()
    return hash

def _compute_root_hash(divs):
    div_hashes = []
    for div in divs:
        div_hashes.append(_compute_hash(div))
    return hashlib.sha256(''.join(div_hashes).encode('ascii')).hexdigest()