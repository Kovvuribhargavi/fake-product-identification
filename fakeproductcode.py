import hashlib
import json
from time import time

class Block:
    def __init__(self, index, timestamp, products, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.products = products
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_products = []

    def create_genesis_block(self):
        return Block(0, time(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, block):
        self.chain.append(block)

    def mine_pending_products(self):
        block = Block(len(self.chain), time(), self.pending_products, self.get_latest_block().hash)
        self.pending_products = []
        self.add_block(block)

    def add_product(self, product):
        self.pending_products.append(product.to_dict())

    def verify_product(self, product):
        for block in self.chain:
            for block_product in block.products:
                if Product.from_dict(block_product) == product:
                    return True
        return False

    def check_for_fake_products(self):
        product_counts = {}
        for block in self.chain:
            for product_dict in block.products:
                product = Product.from_dict(product_dict)
                if product in product_counts:
                    product_counts[product] += 1
                else:
                    product_counts[product] = 1
        
        return [product for product, count in product_counts.items() if count > 1]

class Product:
    def __init__(self, name, manufacturer, serial_number):
        self.name = name
        self.manufacturer = manufacturer
        self.serial_number = serial_number

    def __eq__(self, other):
        return (self.name, self.manufacturer, self.serial_number) == (other.name, other.manufacturer, other.serial_number)

    def __hash__(self):
        return hash((self.name, self.manufacturer, self.serial_number))

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

if __name__ == '__main__':
    blockchain = Blockchain()

    print("Adding products to the blockchain...")
    blockchain.add_product(Product("Apple iPhone 12", "Apple Inc.", "123456"))
    blockchain.add_product(Product("Samsung Galaxy S21", "Samsung Electronics", "789012"))
    blockchain.add_product(Product("Microsoft Surface Laptop 3", "Microsoft Corporation", "345678"))
    blockchain.add_product(Product("Sony PlayStation 5", "Sony Corporation", "901234"))
    blockchain.mine_pending_products()

    print("Verifying products on the blockchain...")
    print("Product verified:", blockchain.verify_product(Product("Apple iPhone 12", "Apple Inc.", "123456")))

    print("Checking for fake products...")
    blockchain.add_product(Product("Apple iPhone 12", "Apple Inc.", "123456"))  # Duplicate product
    blockchain.mine_pending_products()

    fake_products = blockchain.check_for_fake_products()
    print("Fake products found:", [f"{p.name} by {p.manufacturer} with serial {p.serial_number}" for p in fake_products])
