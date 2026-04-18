import hashlib
import json
import time
import os

class BlockchainLogger:
    def __init__(self, filepath="blockchain_ledger.json"):
        self.filepath = filepath
        self.chain = []
        self.load_chain()

    def load_chain(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                try:
                    self.chain = json.load(f)
                except:
                    self.create_genesis_block()
        else:
            self.create_genesis_block()

    def save_chain(self):
        with open(self.filepath, "w") as f:
            json.dump(self.chain, f, indent=4)

    def create_genesis_block(self):
        genesis = {
            "index": 0,
            "timestamp": time.time(),
            "event_data": "Genesis Block - System Initialized",
            "previous_hash": "0",
            "hash": self.hash_block({"index": 0, "previous_hash": "0"})
        }
        self.chain = [genesis]
        self.save_chain()

    def hash_block(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, event_data):
        previous_block = self.chain[-1]
        previous_hash = previous_block["hash"]
        
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "event_data": event_data,
            "previous_hash": previous_hash
        }
        new_block["hash"] = self.hash_block(new_block)
        
        self.chain.append(new_block)
        self.save_chain()
        return new_block
