"""

jerryvmomatic: starts/stops lab VMs (ltraci-2226)


Looking up Managed Object Reference (MoRef) in vCenter Server (1017126)
https://kb.vmware.com/s/article/1017126

"""

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
import ssl
import json
import sys

with open("./vcs.json") as f:
    vcs_list = json.load(f)

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)


def jerry_off(host, pwd):
    c = SmartConnect(
        host=host, user="administrator@vsphere.local", pwd=pwd, sslContext=s
    )
    datacenter = c.content.rootFolder.childEntity[0]
    vms = datacenter.vmFolder.childEntity
    for vm in vms:
        if (
            "student" in vm.name or "asa" in vm.name or "ASA" in vm.name
        ) and "msm" not in vm.name:
            if vm.runtime.powerState == "poweredOn":
                vm.PowerOff()
                print("Jerry is powering off:", vm.name, "on", host)
    Disconnect(c)


def jerry_on(host, pwd):
    c = SmartConnect(
        host=host, user="administrator@vsphere.local", pwd=pwd, sslContext=s
    )
    datacenter = c.content.rootFolder.childEntity[0]
    vms = datacenter.vmFolder.childEntity
    for vm in vms:
        if (
            "student" in vm.name or "asa" in vm.name or "ASA" in vm.name
        ) and "msm" not in vm.name:
            if vm.runtime.powerState == "poweredOff":
                vm.PowerOn()
                print("Jerry is powering on:", vm.name, "on", host)
    Disconnect(c)


def jerry_check(host, pwd):
    c = SmartConnect(
        host=host, user="administrator@vsphere.local", pwd=pwd, sslContext=s
    )
    datacenter = c.content.rootFolder.childEntity[0]
    vms = datacenter.vmFolder.childEntity
    for vm in vms:
        if (
            "student" in vm.name or "asa" in vm.name or "ASA" in vm.name
        ) and "msm" not in vm.name:
            print("Jerry says", vm.name, "is", vm.runtime.powerState, "on", host)
    Disconnect(c)


def jerry_disconnect(host, pwd):
    c = SmartConnect(
        host=host, user="administrator@vsphere.local", pwd=pwd, sslContext=s
    )
    datacenter = c.content.rootFolder.childEntity[0]
    vms = datacenter.vmFolder.childEntity
    for vm in vms:
        if "student" in vm.name:
            #    print("Jerry says", vm.name, "is", vm.network, "on", host)
            print(vm.network[1])

    Disconnect(c)


if __name__ == "__main__":
    try:
        if (sys.argv[1]) == "check":
            for vc in vcs_list:
                jerry_check(vc["ip"], vc["passwd"])
        if (sys.argv[1]) == "off":
            for vc in vcs_list:
                jerry_off(vc["ip"], vc["passwd"])
        if (sys.argv[1]) == "on":
            for vc in vcs_list:
                jerry_on(vc["ip"], vc["passwd"])
        if (sys.argv[1]) == "disconnect":
            for vc in vcs_list:
                jerry_disconnect(vc["ip"], vc["passwd"])
    except:
        print("Jerry is not happy at all")
