
mac_length = 12

def mac_address_from_identifier(identifier):
    str_identifier = str(identifier)
    identifier_length = str_identifier.__len__()

    mac_address = ""
    for i in range(0, mac_length - identifier_length):
        mac_address = mac_address + "0"
    mac_address = mac_address + str_identifier

    # from '000000000001' to '00:00:00:00:00:01'
    mac_address = ":".join(a + b for a, b in zip(mac_address[::2], mac_address[1::2]))

    return mac_address

def identifier_from_mac_address(mac_address):
    mac_address = mac_address.replace(":", "")
    identifier = int(mac_address)
    return identifier

def switch_from_identifier(identifier):
    switch_identifier = "S" + str(identifier)
    return switch_identifier

def host_from_identifier(identifier):
    host_identifier = "H" + str(identifier)
    return host_identifier
