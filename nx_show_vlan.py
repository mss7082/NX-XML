#!/usr/bin/env python

# This code outputs the current list of vlans configured on Nexus switches using NETCONF Protocol.
# created by Moses Sokabi, Jan 2nd, 2015

from ncclient import manager
import xmltodict

ip_list = ['172.16.1.105']
user = 'admin'
password = 'admin'
port = 22

# XML code  to show current vlans using Nexus embedded XMLIN tool
cmd_show_vlans = '''
        <show>
            <vlan/>
        </show>'''

vlan_result_list = []           # Used to separate results per IP into a list, for easy call later

# Append results for each IP address in the list
def show_vlans(cmd):
    for ip in ip_list:
        with manager.connect(host=ip, username=user, password=password, port=port, device_params={'name':'nexus'}) as m:
            result = m.get(('subtree', cmd))
            vlan_result_list.append(result)
    for i,n in enumerate(vlan_result_list):
        xml_raw = vlan_result_list[i]
        result_dict = xmltodict.parse(str(xml_raw)) # Convert to string XMLTODICT required xml_raw to be string
        show_vlan_path = result_dict['rpc-reply']['data']['mod:show']['mod:vlan'] \
                ['mod:__XML__OPT_Cmd_show_vlan___readonly__']['mod:__readonly__']['mod:TABLE_vlanbrief']['mod:ROW_vlanbrief']
        for vlan_details in show_vlan_path:
            vlan_id = vlan_details['mod:vlanshowbr-vlanid-utf']
            vlan_name = vlan_details['mod:vlanshowbr-vlanname']
            vlan_state = vlan_details['mod:vlanshowbr-vlanstate']
            print 'VLAN ' + vlan_id + ' named ' + vlan_name + ' is ' + vlan_state
    print 'On ' + ip

show_vlans(cmd_show_vlans)
