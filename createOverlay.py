import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# LOGIN CREDENTIALS

apic = "https://sandboxapicdc.cisco.com"
user = "admin"
pwd = "ciscopsdt"

# DEFINE FUNCTIONS

def login():
    url = apic + "/api/aaaLogin.json"
    payload = {"aaaUser":{"attributes":{"name": user,"pwd": pwd}}}
    header = {"content-type": "application/json"}
                    
    r = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    r_json = r.json()

    auth_token = r_json["imdata"][0]["aaaLogin"]["attributes"]["token"]
    cookie = {"APIC-Cookie": auth_token}
    return cookie

def createTenant(tenant, cookie):
    url = apic + "/api/node/mo/uni/tn-" + tenant + ".json"
    header = {"content-type": "application/json"}
    payload = {
                "fvTenant": {
                    "attributes": {
                        "name": tenant,
                        "status": "created"
                        }
                    }
                }

    r = requests.post(url, data=json.dumps(payload), cookies=cookie, headers=header, verify=False)

    if r.status_code == 200:
        print("[+] tenant tn-" + tenant + " was created.")
    elif r.status_code == 400:
        print("[-] tenant tn-" + tenant + " was not created.")

def createApp(tenant, app, cookie):
    url = apic + "/api/node/mo/uni/tn-" + tenant + "/ap-" + app + ".json"
    header = {"content-type": "application/json"}
    payload = {
                "fvAp": {
                    "attributes": {
                        "name": app,
                        "status": "created"
                        }
                    }
                }
    r = requests.post(url, data=json.dumps(payload), cookies=cookie, headers=header, verify=False)

    if r.status_code == 200:
        print("[+] aplication profile " + app + " was created.")
    elif r.status_code == 400:
        print("[-] aplication profile " + app + " was not created.")

def createVrf(tenant, vrf, cookie):
    url = apic + "/api/node/mo/uni/tn-" + tenant + "/ctx-" + vrf + ".json"
    header = {"content-type": "application/json"}
    payload = {
                "fvCtx": {
                    "attributes": {
                        "name": vrf,
                        "status": "created"
                        }
                    }
                }

    r = requests.post(url, data=json.dumps(payload), cookies=cookie, headers=header, verify=False)

    if r.status_code == 200:
        print("[+] VRF " + vrf + " was created.")
    elif r.status_code == 400:
        print("[-] VRF profile " + vrf + " was not created.")

def createBd(tenant, vrf, bd, cookie):
    url = apic + "/api/node/mo/uni/tn-" + tenant + "/BD-" + bd + ".json"
    header = {"content-type": "application/json"}
    payload = {
                "fvBD": {
                    "attributes": {
                        "name":bd,
                        "status":"created"
                        },
                    "children": [
                        {
                            "fvRsCtx": {
                                "attributes": {
                                    "tnFvCtxName": vrf,
                                    "status": "created,modified"
                                    }
                                }
                            }
                        ]
                    }
                }

    r = requests.post(url, data=json.dumps(payload), cookies=cookie, headers=header, verify=False)

    if r.status_code == 200:
        print("[+] Bridge domain " + bd + " was created.")
    elif r.status_code == 400:
        print("[-] Bridge domain " + bd + " was not created.")

def createEpg(tenant, app, epg, bd, cookie):
    url = apic + "/api/node/mo/uni/tn-" + tenant + "/ap-" + app + "/epg-" + epg + ".json"
    header = {"content-type": "application/json"}
    payload = {
                "fvAEPg": {
                    "attributes": {
                        "name":epg,
                        "status":"created"
                        },
                    "children": [
                        {
                            "fvRsBd": {
                                "attributes": {
                                    "tnFvBDName": bd,
                                    "status":"created,modified"
                                    }
                                }
                            }
                        ]
                    }
                }

    r = requests.post(url, data=json.dumps(payload), cookies=cookie, headers=header, verify=False)

    if r.status_code == 200:
        print("[+] EPG " + epg + " was created.")
    elif r.status_code == 400:
        print("[-] EPG " + epg + " was not created.")
           
# EXECUTE TASKS

cookie = login()
tenants = ["hirvi", "karhu", "janis", "koira"]

for tenant in tenants:
    print("[!] Create overlay: " + tenant.upper())
    createTenant(tenant, cookie)
    app = "ap-" + tenant
    createApp(tenant, app, cookie)
    vrf = "vrf-" + tenant
    createVrf(tenant, vrf, cookie)
    bd = "bd-" + tenant
    createBd(tenant, vrf, bd, cookie)
    for i in range(2):
        epg = "epg-" + tenant + "-" + str(i)
        createEpg(tenant, app, epg, bd, cookie)
    print("[!] Moving to the next overlay")
    print("\n")
        


