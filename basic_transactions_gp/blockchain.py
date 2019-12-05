# Paste your version of blockchain.py from the basic_block_gp
# folder here

import hashlib
import json
from time import time
from uuid import uuid4
from flask_cors import CORS
from flask import Flask, jsonify, request

DIFFICULTY = 3

"""
1) function for creating as new block with required info - new_block
2) function to hash a previous block into a new hash string, repeatedly, until certain criteria are met - valid_proof
3) function that calls/invokes hashing function - proof_of_work
"""

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            # TODO
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It convertes the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        block_string = json.dumps(block, sort_keys=True).encode()
        # TODO: Hash this string using sha256
        hash = hashlib.sha256(block_string).hexdigest()
        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hash

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     # TODO
    #     # Take last_block, jsonify it, run it thru valid_proof until it comes out as true
    #     block_string = json.dumps(self.last_block, sort_keys=True)
    #     proof = 0
    #     while self.valid_proof(block_string, proof) is False:
    #         proof += 1
    #     return proof
    #     # return proof

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # encode needed to format into something comp can understand
        # hexdigest decodes it.  Don't ask, its just the way things are
        # with python

        # Hash the given block string until it has 3 leading zeroes.  Return the result
        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # return True or False - [:3] = slice off first 3 digits
        return guess_hash[:DIFFICULTY] == "0" * DIFFICULTY

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

# Instantiate our Node
app = Flask(__name__)
CORS(app)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route("/transactions/new", methods=["POST"])
def post_new_transaction():
    try:
        data = request.get_json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
        return "Error"
    if data["sender"] and data["recipient"] and data["amount"]:
        blockchain.new_transaction(
            data["sender"], 
            data["recipient"], 
            data["amount"]
            )
        message = {
            "block_index": blockchain.last_block["index"],
            "block": blockchain.last_block
        }
        return jsonify(message), 200
@app.route('/mine', methods=['POST'])
def mine():
    try:
        data = request.get_json()
    #print("Endpoint has been hit")
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
        return "Error"
    #print("Data proof is ", data["proof"])
    if data["proof"] and data["id"]:
        print("Got thru if-statement")
        previous = blockchain.hash(blockchain.last_block)
        new = blockchain.new_block(data["proof"], previous)
        blockchain.new_transaction("0", data["id"], 1)
        response = {
            "Success": new
        }
        return jsonify(response), 400
    else:
        print("Failure")
        response = {"Failure": data}
        return jsonify(response), 404

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        "length": len(blockchain.chain),
        "chain": blockchain.chain,
    }
    return jsonify(response), 200

@app.route('/last_block', methods=['GET'])
def lastBlock():
    response = {
        # TODO: Return the chain and its current length
        "last_block": blockchain.last_block
    }
    return jsonify(response), 200



# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
