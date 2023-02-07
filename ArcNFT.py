import hashlib,uuid
from pinatapy import PinataPy
from mimetypes import MimeTypes
from algosdk.v2client import algod
from nacl.signing import SigningKey
from .NFT_CONFIGS import ARC3,ARC69
from .util import ipfs_file_integrity
from multiformats_cid import make_cid
from algosdk.error import AlgodHTTPError
from algosdk.encoding import encode_address
from algosdk.transaction import (AssetConfigTxn,AssetUpdateTxn)
from algosdk import account

class ARCNFT():
    """A simple NFT ARC SDK for minting and updating Algorand NFTs"""

    def __init__(self,algodToken:str,pinata_api_key:str, pinata_secret_key:str,network:str = "testnet") -> None:
        self.network = network
        self.token = algodToken
        self.mime = MimeTypes()

        self.headers = {
        "X-API-Key": self.token,
        }

        if 'main' in self.network:
            self.network_endpoint = "https://mainnet-algorand.api.purestake.io/ps2"
        else:
            self.network_endpoint = "https://testnet-algorand.api.purestake.io/ps2"

        self.pinata = PinataPy(pinata_api_key, pinata_secret_key)
        self.client = algod.AlgodClient(self.token,self.network_endpoint,self.headers)
    
    def create_arc3_nft(self,creator,creator_key,*args,**kwargs):
        """This method is for creating an Arc3 nft"""

        filePath = kwargs.get("filePath",None)
        name = str(kwargs.get("name",uuid.uuid4()))
        description = str(kwargs.get("description",uuid.uuid4()))

        if filePath == None:
            return("filePath is needed")
        
        IPFS = self.pinata.pin_file_to_ipfs(filePath)
        ipfsHash = IPFS.get("IpfsHash")

        ARC3["name"] = f"{name}"
        ARC3["description"] = description
        ARC3["image"] = f"ipfs://{ipfsHash}"
        ARC3["image_integrity"] = f"sha256-{ipfs_file_integrity(ipfsHash)}"
        ARC3["image_mimetype"] = f"{self.mime.guess_type(filePath)[0]}"
        ARC3["properties"]["file_url_integrity"] = f"sha256-{ipfs_file_integrity(ipfsHash)}"
        ARC3["properties"]["file_url_mimetype"] = f"{self.mime.guess_type(filePath)[0]}"

        IPFSJson = self.pinata.pin_json_to_ipfs(ARC3)
        JsonHash = IPFSJson.get("IpfsHash")

        hash = hashlib.new("sha512_256")
        hash.update(b"arc0003/amj")
        hash.update(str(ARC3).encode("utf-8"))
        json_metadata_hash = hash.digest()
        txn_params = self.client.suggested_params()

        txn = AssetConfigTxn(
            sender=creator,
            sp=txn_params,
            total=1,
            default_frozen=False,
            unit_name=kwargs.get("symbol"),
            asset_name=name,
            manager=kwargs.get("manager",creator),
            reserve=kwargs.get("reserve",creator),
            freeze=kwargs.get("freeze",creator),
            clawback=kwargs.get("clawback",creator),
            strict_empty_address_check=False,
            url=f"ipfs://{JsonHash}#arc3", 
            metadata_hash=json_metadata_hash,            
            decimals=0)
    
        stxn = txn.sign(creator_key)
        txid = self.client.send_transaction(stxn)
        return({"transactionHash":txid})

    def create_arc69_nft(self,creator,creator_key,*args,**kwargs):
        """This method is for creating an Arc69 nft"""
        filePath = kwargs.get("filePath",None)
        publisher = kwargs.get("publisher","")
        royalties = kwargs.get("royalties",[])
        description = kwargs.get("description","")
        name = str(kwargs.get("name",uuid.uuid4()))
        creator_name = kwargs.get("creator_name","")
        symbol = str(kwargs.get("symbol",uuid.uuid4()))
        creator_desciption = str(kwargs.get("creator_desciption",uuid.uuid4()))

        
        royalties.append({"name":"creator","addr":creator,"share":5})

        if filePath == None:
            return("filePath is needed")
        
        IPFS = self.pinata.pin_file_to_ipfs(filePath)
        ipfsHash = IPFS.get("IpfsHash")

        ARC69["properties"]["royalties"] = royalties
        ARC69["properties"]["publisher"] = publisher
        ARC69["properties"]["creator"]["address"] = creator
        ARC69["properties"]["creator"]["name"] = creator_name
        ARC69["properties"]["creator"]["description"] = creator_desciption
        
        ARC69["name"] = f"{name}"
        ARC69["assetName"] = f"{name}"
        ARC69["unitName"] = f"{symbol}"
        ARC69["description"] = description
        ARC69["image"] = f"ipfs://{ipfsHash}"
        ARC69["image_integrity"] = f"sha256-{ipfs_file_integrity(ipfsHash)}"
        ARC69["image_mimetype"] = f"{self.mime.guess_type(filePath)[0]}"
        ARC69["properties"]["file_url_integrity"] = f"sha256-{ipfs_file_integrity(ipfsHash)}"
        ARC69["properties"]["file_url_mimetype"] = f"{self.mime.guess_type(filePath)[0]}"

        IPFSJson = self.pinata.pin_json_to_ipfs(ARC69)
        JsonHash = IPFSJson.get("IpfsHash")

        hash = hashlib.new("sha512_256")
        hash.update(b"arc0069/amj")
        hash.update(str(ARC3).encode("utf-8"))
        json_metadata_hash = hash.digest()
        txn_params = self.client.suggested_params()

        txn = AssetConfigTxn(
            sender=creator,
            sp=txn_params,
            total=1,
            default_frozen=False,
            unit_name=symbol,
            asset_name=name,
            manager=kwargs.get("manager",creator),
            reserve=kwargs.get("reserve",creator),
            freeze=kwargs.get("freeze",creator),
            clawback=kwargs.get("clawback",creator),
            strict_empty_address_check=False,
            url=f"ipfs://{JsonHash}", 
            metadata_hash=json_metadata_hash,            
            decimals=0)
    
        stxn = txn.sign(creator_key)
        txid = self.client.send_transaction(stxn)
        return({"transactionHash":txid})
    
    def create_arc19_nft(self,creator,creator_key,*args,**kwargs):
        """This method is for creating an Arc19 nft this uses the ARC3 Format"""

        filePath = kwargs.get("filePath",None)
        name = str(kwargs.get("name",uuid.uuid4()))
        description = str(kwargs.get("description",uuid.uuid4()))

        if filePath == None:
            return("filePath is needed")
        
        IPFS = self.pinata.pin_file_to_ipfs(filePath)
        ipfsHash = IPFS.get("IpfsHash")

        ARC3["name"] = f"{name}"
        ARC3["description"] = description
        ARC3["image"] = f"ipfs://{ipfsHash}"
        ARC3["image_integrity"] = f"sha256-{ipfs_file_integrity(ipfsHash)}"
        ARC3["image_mimetype"] = f"{self.mime.guess_type(filePath)[0]}"
        ARC3["properties"]["file_url_integrity"] = f"sha256-{ipfs_file_integrity(ipfsHash)}"
        ARC3["properties"]["file_url_mimetype"] = f"{self.mime.guess_type(filePath)[0]}"

        IPFSJson = self.pinata.pin_json_to_ipfs(ARC3)
        JsonHash = IPFSJson.get("IpfsHash")
        cid = make_cid(JsonHash)
        pid = cid.multihash.hex()[4:]
        hash = hashlib.new("sha512_256")
        hash.update(b"arc0003/amj")
        hash.update(str(ARC3).encode("utf-8"))
        json_metadata_hash = hash.digest()
        txn_params = self.client.suggested_params()

        
        txn = AssetConfigTxn(
            sender=creator,
            sp=txn_params,
            total=1,
            default_frozen=False,
            unit_name=kwargs.get("symbol"),
            asset_name=name,
            manager=kwargs.get("manager",creator),
            reserve=self.__algorand_address_from_ipfsHash(pid),
            freeze=kwargs.get("freeze",creator),
            clawback=kwargs.get("clawback",creator),
            strict_empty_address_check=False,
            url=f"template-ipfs://{{ipfscid:{cid.version}:{cid.codec}:reserve:sha2-256}}", 
            metadata_hash=json_metadata_hash,            
            decimals=0)
    
        stxn = txn.sign(creator_key)
        txid = self.client.send_transaction(stxn)
        return({"transactionHash":txid})

    def __algorand_address_from_ipfsHash(self,hash:str)->dict:
        """Receives HEX as key then returns an equivalent algorand wallet"""
        secret_key  = bytes.fromhex(hash)
        signing_key = SigningKey(secret_key)
        sk = signing_key
        vk = signing_key.verify_key
        algod_address = encode_address(vk.encode())
        return(algod_address)

    def update_arc_nft(self,*args, **kwargs):
        """A method to update an already existing algorand ARC NFT"""

        assetID = kwargs.get("asset_id",None)
        if assetID == None:
            return("Asset ID is needed")

        try:
            asset = self.client.asset_info(assetID)['params']
        except AlgodHTTPError as e:
            return(f"{str(e)}")

        creator = kwargs.get("creator",asset.get("creator"))
        txn_params = self.client.suggested_params()

        txn = AssetUpdateTxn(
            sender=creator,
            sp=txn_params,
            manager=kwargs.get("new_manager",creator),
            reserve=kwargs.get("new_reserve",creator),
            freeze=kwargs.get("new_freeze",None),
            clawback=kwargs.get("new_clawback",None),
            index=assetID
            )
        stxn = txn.sign(kwargs.get("creator_key"))
        txid = self.client.send_transaction(stxn)
        return({"transactionHash":txid})
