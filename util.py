import base64,base58,binascii



def ipfs_file_integrity(cid):
    """Converts a CID to a base64 file hash"""
    decoded = base58.b58decode(cid)
    sliced_decoded = decoded[2:]

    return(binascii.b2a_base64(sliced_decoded).decode("ascii"))

def ipfscidv0_to_byte32(cid):
    """
    Convert ipfscidv0 to 32 bytes hex string.
    Args:
        cid (string): IPFS CID Version 0
    Returns:
        str: 32 Bytes long string
    """
    """bytes32 is converted back into Ipfs hash format."""

    decoded = base58.b58decode(cid)
    sliced_decoded = decoded[2:]
    return binascii.b2a_hex(sliced_decoded).decode("utf-8")


def byte32_to_ipfscidv0(hexstr):
    """
    Convert 32 bytes hex string to ipfscidv0.
    Args:
        hexstr (string): 32 Bytes long string
    Returns:
        str: IPFS CID Version 0
    """

    binary_str = binascii.a2b_hex(hexstr)
    completed_binary_str = b'\x12 ' + binary_str
    return(base58.b58encode(completed_binary_str))