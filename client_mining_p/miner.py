import hashlib
import requests

import sys
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

DIFFICULTY = 3

"""
1) Provide proof_of_work with the hash of previous block
2) proof_of_work will stringify it, and send it to valid_proof
3) valid_proof will run until it finds the requisite hash, then send it back
4) proof_of_work will return the proof only
"""

def proof_of_work(last_block):
        """
        Simple Proof of Work Algorithm
        Stringify the block and look for a proof.
        Loop through possibilities, checking each one against `valid_proof`
        in an effort to find a number that is a valid proof
        :return: A valid proof for the provided block
        """
        # TODO
        # Take last_block, jsonify it, run it thru valid_proof until it comes out as true
        block_string = json.dumps(last_block, sort_keys=True)
        proof = 0
        print("Starting proof_of_work")
        while valid_proof(block_string, proof) is False:
            proof += 1
        print("Finished proof_of_work")
        return proof
        # return proof


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


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run forever until interrupted
    # while True:
    count = 0
    coins = 0
    while count < 5:
        count += 1
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            print("Count is ", count)
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        #print("Got thru try-except")
        #print("Data is ", data)
        #print("Data last block is ", data["last_block"])
        new_proof = proof_of_work(data["last_block"])
        coins += 1
        print("New Proof found, coins are: ", coins)

        # When found, POST it to the server {"proof": new_proof, "id": id}

        post_data = {"proof": new_proof, "id": id}
        #print("Post_data is ", post_data)
        r = requests.post(url=node + "/mine", json = post_data) 
        try:
            data = r.json()
            print("Data back from post is ", data)
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        f = open("my_id.txt", "r+")
        name = f.write("Name: Greg")
        print("Name is ", name)
        f.close()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        
