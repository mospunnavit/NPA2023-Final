from ncclient import manager
import xmltodict

m = manager.connect(
    host="10.0.15.182",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )

def create():
    netconf_config = """<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback>
    <name>65070135</name>
    <description>My first NETCONF loopback</description>
    <ip>
     <address>
      <primary>
       <address>172.30.135.1</address>
       <mask>255.255.255.0</mask>
      </primary>
     </address>
    </ip>
   </Loopback>
  </interface>
 </native>
</config>"""

    if status() == "not found":
        try:
            netconf_reply = netconf_edit_config(netconf_config)
            xml_data = netconf_reply.xml
            print(xml_data)
            if '<ok/>' in xml_data:
                return "Interface loopback 65070135 is created successfully"
        except:
            print("Cannot create: Interface loopback 65070135")
    else:
        return "Cannot create: Interface loopback 65070135"

def delete():
    netconf_config = """<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback operation="delete">
    <name>65070135</name>
   </Loopback>
  </interface>
 </native>
</config>"""
    if status() == "found":
        try:
            netconf_reply = netconf_edit_config(netconf_config)
            xml_data = netconf_reply.xml
            print(xml_data)
            if '<ok/>' in xml_data:
                return "Interface loopback 65070135 is deleted successfully"
        except:
            print("Error!")
    else:
        return "Cannot delete: Interface loopback 65070135"

def enable():
    netconf_config = """<!!!REPLACEME with YANG data!!!>"""

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "<!!!REPLACEME with proper message!!!>"
    except:
        print("Error!")


def disable():
    netconf_config = """<!!!REPLACEME with YANG data!!!>"""

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "<!!!REPLACEME with proper message!!!>"
    except:
        print("Error!")

def netconf_edit_config(netconf_config):
    return  m.edit_config(target="running", config=netconf_config)


def status():
    netconf_filter = """<filter>
 <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
 <interface><name>Loopback65070135</name></interface>
 </interfaces-state>
</filter>"""
    print("s1")
    # Use Netconf operational operation to get interfaces-state information
    netconf_reply = m.get(filter=netconf_filter)
    print(netconf_reply)
    netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
    print(netconf_reply_dict)
    print(type(netconf_reply_dict.get('rpc-reply', {}).get('data')))
    #if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
    if netconf_reply_dict.get('rpc-reply', {}).get('data') is not None:
        # extract admin_status and oper_status from netconf_reply_dict
        interface_data = netconf_reply_dict['rpc-reply']['data']['interfaces-state']['interface']
        admin_status = interface_data['admin-status']
        oper_status = interface_data['oper-status']
        if admin_status == 'up' and oper_status == 'up':
            return "found"
        elif admin_status == 'down' and oper_status == 'down':
            return "found"
    else: # no operation-state data
        return "not found"
       

    