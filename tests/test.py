# _*_ coding:utf-8 _*_

from osapi import *

import requests
from osapi.sdnapi import Controller, BASE_URL, StaticFlowPusher
from osapi.sdnapi.settings import OPENFLOWDB_CONN


# print requests.get("http://192.168.1.180:8008/metric/192.168.1.170/json").json()
# metric_json = {
#  "12.ifadminstatus": "up",
#  "5.ifindex": "5",
#  "2.1000.app_fd_open": 0,
#  "12.ifoutpkts": 1.2,
#  "15.ifdirection": "full-duplex",
#  "20.ifinoctets": 0,
#  "20.ifoutdiscards": 0,
#  "2.1000.app_fd_max": 0,
#  "12.ifdirection": "full-duplex",
#  "2.1000.app_mem_used": 51789824,
#  "2.1000.ovs_dp_masks": 4,
#  "12.ifinpkts": 1,
#  "15.ifindiscards": 0,
#  "20.ifinerrors": 0,
#  "15.of_port": "3",
#  "15.ifname": "qvodc6c9287-74",
#  "2.1000.ovs_dp_misses": 0,
#  "15.ifinmulticastpkts": 0,
#  "5.ifinerrors": 0,
#  "20.ifname": "qvoa96c58d9-bf",
#  "15.ifindex": "15",
#  "20.ifdirection": "full-duplex",
#  "20.ifinpkts": 0,
#  "12.of_port": "2",
#  "15.ifadminstatus": "up",
#  "20.ifspeed": 10000000000,
#  "15.ifspeed": 10000000000,
#  "20.ifinutilization": 0,
#  "12.iftype": "ethernetCsmacd",
#  "5.ifspeed": 100000000,
#  "20.ifoutpkts": 0.19998000199980004,
#  "20.ifindex": "20",
#  "15.ifoperstatus": "up",
#  "2.1000.ovs_dp_maskhitsperpacket": 3.3181818181818183,
#  "5.iftype": "ethernetCsmacd",
#  "12.ifindex": "12",
#  "5.ifouterrors": 0,
#  "2.1000.app_usertime": 0.12001200120012002,
#  "12.49cb41c2-8d7e-4a2b-b9b8-0922f0df4713": 1.0611994482406207E-25,
#  "15.ifinucastpkts": 0,
#  "15.ifoutpkts": 0.19998000199980004,
#  "5.ifoutdiscards": 0,
#  "2.1000.ovs_mask_hits": 7.3007300730073,
#  "12.of_dpid": "00007294fc095d43",
#  "12.ifinoctets": 98,
#  "20.iftype": "ethernetCsmacd",
#  "5.ifdirection": "unknown",
#  "2.1000.ovs_dp_flows": 4,
#  "15.ifoutoctets": 15.798420157984202,
#  "2.1000.ovs_dp_missrate": 0,
#  "12.ifoperstatus": "up",
#  "15.ifinerrors": 0,
#  "5.ifoutoctets": 0,
#  "20.ifadminstatus": "up",
#  "5.ifoututilization": 0,
#  "20.ifindiscards": 0,
#  "15.ifoutucastpkts": 0.19998000199980004,
#  "12.ifoutoctets": 113.8,
#  "15.ifinpkts": 0,
#  "5.ifindiscards": 0,
#  "20.ifinmulticastpkts": 0,
#  "20.ifouterrors": 0,
#  "12.ifspeed": 10000000000,
#  "5.ifadminstatus": "down",
#  "2.1000.ovs_dp_hits": 2.2002200220022,
#  "15.ifinoctets": 0,
#  "2.1000.ovs_dp_lost": 0,
#  "20.ifoperstatus": "up",
#  "5.ifinucastpkts": 0,
#  "12.ifouterrors": 0,
#  "20.of_dpid": "00007294fc095d43",
#  "12.ifoutucastpkts": 1.2,
#  "5.ifoutpkts": 0,
#  "20.ifinucastpkts": 0,
#  "12.ifinerrors": 0,
#  "5.of_dpid": "00007294fc095d43",
#  "12.ifoutdiscards": 0,
#  "15.of_dpid": "00007294fc095d43",
#  "15.ifouterrors": 0,
#  "5.ifinoctets": 0,
#  "5.of_port": "65534",
#  "20.ifoutucastpkts": 0.19998000199980004,
#  "20.of_port": "4",
#  "15.ifoututilization": 1.2638736126387362E-6,
#  "15.ifinutilization": 0,
#  "5.ifoperstatus": "down",
#  "2.1000.app_systemtime": 0.040004000400040006,
#  "12.ifinutilization": 7.84E-6,
#  "5.ifoutucastpkts": 0,
#  "20.ifoututilization": 1.2638736126387362E-6,
#  "12.ifinmulticastpkts": 0,
#  "2.1000.app_conn_open": 0,
#  "2.1000.ovs_dp_hitrate": 100,
#  "12.ifindiscards": 0,
#  "12.ifname": "qvoff9715cf-22",
#  "12.ifoututilization": 9.104E-6,
#  "15.ifoutdiscards": 0,
#  "5.ifinmulticastpkts": 0,
#  "12.ifinucastpkts": 1,
#  "2.1000.app_mem_max": 0,
#  "15.iftype": "ethernetCsmacd",
#  "5.ifname": "br-int",
#  "2.1000.app_conn_max": 0,
#  "5.ifinutilization": 0,
#  "20.ifoutoctets": 15.798420157984202
# }
# index = ""
# for key, val in metric_json.items():
#     if val == "qvodc6c9287-74":
#         index = key.split('.')[0]
#         break
#
# print metric_json[index+".of_port"]

if __name__ == "__main__":
    # controller = Controller(BASE_URL)
    # switch_json = controller.get_switches()
    # print json.dumps(switch_json)
    # of_dpid = ""
    # for switch in switch_json:
    #     if switch["inetAddress"].startswith("/192.168.1.171"):
    #         of_dpid = switch["switchDPID"]
    #         break
    # print of_dpid
    print ""
