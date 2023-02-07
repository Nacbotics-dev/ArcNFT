# ArcNFT-SDK
an unofficial sdk for the ALgorand ARC nft

### This sdk is for the python devs


### Supported Algorand NFT ARCs

- **ARC3**
  - <https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md>

- **ARC19**
  - <https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0019.md>

- **ARC69**
  - <https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0069.md>

### Code examples

import the SDK
```
from SDK.ArcNFT import ARCNFT
```

```
arcNFT = ARCNFT(algodToken=<algodToken>,pinata_api_key=<pinata_api_key>,pinata_secret_key=<pinata_secret_key>)
```


To create an ARC3 NFT

```
myArc3NFT = arcNFT.create_arc3_nft(
    creator=address,
    creator_key=private_key,
    filePath=filePath,name="yani yannu",
    symbol="Yanyan",
    description="Beauty Goddess"
)
```

To create an ARC19 NFT

```
myArc19NFT = arcNFT.create_arc19_nft(
    creator=address,
    creator_key=private_key,
    filePath=filePath,
    name="Ha mulan",
    symbol="HaM",
    description="The warrior queen",
    creator_name="Supreme leader")
```

To create an ARC69 NFT

```
myArc69NFT = arcNFT.create_arc69_nft(
    creator=address,
    creator_key=private_key,
    filePath=filePath,
    name="Lady warrior",
    symbol="LWA",
    description="The blooming princess",
    creator_name="Supreme leader")
```



To update an ARC NFT

```
updateMYNFT = arcNFT.update_arc_nft(asset_id="157574395",creator_key=private_key)
```

#### Note: the parameters parsed here are just to create a basic ARC nft please referr to the SDK codes to know about more paramaters
