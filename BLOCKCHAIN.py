import json
from hashlib import sha256
from datetime import datetime
class Block:
    def __init__(self,index,previous_hash,current_transactions,timestamp,nonce):
        self.index=index
        self.previous_hash=previous_hash
        self.current_transactions=current_transactions
        self.timestamp=timestamp
        self.nonce=nonce
        self.hash=self.compute_hash()
    def compute_hash(self):
        block_string=json.dumps(self.__dict__,sort_keys=True) #converting dict to string
        first_hash=sha256(block_string.encode()).hexdigest()
        second_hash=sha256(first_hash.encode()).hexdigest()
        return second_hash
    def __str__(self):
        return str(self.__dict__)
class Blockchain:
    def __init__(self):
        self.chain=[]
        self.transactions=[]
        self.genesis_block()  #this returns object of Block (ie. first block named genesis) everytime object of blockchain is created
        #this means creating an object of Blockchain automatically creates an object of Block
    def __str__(self):
        return str(self.__dict__)
    def genesis_block(self):
        genesis_block=Block("Genesis",0x0,[3,4,5,6,7],datetime.now().timestamp(),0)
        self.chain.append(genesis_block.hash)
        self.transactions.append(genesis_block.__dict__)
        return genesis_block
    def get_last_block(self):
        return self.chain[-1]
    def proof_of_work(self,block):
        difficulty=1
        block.nonce=0
        computed_hash=block.compute_hash()
        while not (computed_hash.endswith("0"*difficulty) and ("55"*difficulty) in computed_hash):
            block.nonce+=1
            computed_hash=block.compute_hash()
        return computed_hash
    def add_block(self,data):
        block=Block(len(self.chain),self.chain[-1],data,datetime.now().timestamp(),0)
        block.hash=self.proof_of_work(block)
        self.chain.append(block.hash)
        self.transactions.append(block.__dict__)
    def get_transactions(self,id):
        labels=["Manufacturer","Transportation","Retailer"]
        try:
            if id=="all":
                for i in range(len(self.transactions)-1):
                    print(f"{labels[i]}:{self.transactions[i+1]}")
            elif type(id)==int:
                print(self.transactions[id])
            else:
                raise Exception("give valid input")
        except Exception as e:
            print(e)
def main():
    manufacturer=     {"transactions":[{"timestamp":datetime.now().timestamp(),"product id":1,"product serial":50001000,
                                    "name":"cotton pants","from":"Manufacturer X","to":"Transportation X",
                                    "message":"this product is in good order","digital signature":"approved","flagged":"N"},
                                    {"timestamp":datetime.now().timestamp(),"product id":2,"product serial":50001001,
                                    "name":"cotton pants","from":"Manufacturer X","to":"Transportation X",
                                    "message":"this product is in good order","digital signature":"approved","flagged":"N"},
                                    {"timestamp":datetime.now().timestamp(),"product id":3,"product serial":50001002,
                                    "name":"cotton pants","from":"Manufacturer X","to":"Transportation X",
                                    "message":"this product is in good order","digital signature":"approved","flagged":"N"}]}
    Transportation=   {"transactions":[{"timestamp":datetime.now().timestamp(),"product id":1,"product serial":50001000,
                                    "name":"cotton pants","from":"Manufacturer X","to":"Transportation X","shipping id":239,
                                    "message":"this product is in good order","digital signature":"approved","flagged":"N"},
                                    {"timestamp":datetime.now().timestamp(),"product id":2,"product serial":50001001,
                                    "name":"cotton pants","from":"Manufacturer X","to":"Transportation X","shipping id":219,
                                    "message":"this product is in good order","digital signature":"approved","flagged":"N"},
                                    {"timestamp":datetime.now().timestamp(),"product id":3,"product serial":50001002,
                                    "name":"cotton pants","from":"Transportation X","to":"Retailer  X","shipping id":123,
                                    "message":"product damaged","digital signature":"Retailer review","flagged":"Y"}]}
    Retailer=         {"transactions":[{"timestamp":datetime.now().timestamp(),"product id":1,"product serial":50001000,
                                    "name":"cotton pants","from":"Manufacturer X","to":"Transportation X","receiving id":234,
                                    "message":"this product is in good order","digital signature":"approved","flagged":"N"},
                                    {"timestamp":datetime.now().timestamp(),"product id":2,"product serial":50001001,
                                    "name":"cotton pants","from":"Manufacturer X","to":"Transportation X","receiving id":299,
                                    "message":"this product is in good order","digital signature":"approved","flagged":"N"},
                                    {"timestamp":datetime.now().timestamp(),"product id":3,"product serial":50001002,
                                    "name":"cotton pants","from":"Retailer X","to":"RETURN TO VENDOR ","receiving id":284,
                                    "message":"DAMAGED","digital signature":"REJECTED","flagged":"Y"}]}
    B=Blockchain()
    B.add_block(manufacturer)
    B.add_block(Transportation)
    B.add_block(Retailer)
    B.get_transactions("all")
if __name__=="__main__":
    main()