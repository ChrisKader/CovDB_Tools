#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import json
import time
import datetime
import requests
import signal
import pymongo
from pymongo import MongoClient
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import TokenExpiredError

addon_version = '1.1.0'
interface_version = '90002'
addon_path = "./CovDB_Addon"

try:
    import tokens
except ImportError:
    print("[ERROR] Create a credentials file tokens.py with:")
    print("[ERROR]   tokens = {")
    print("[ERROR]     'covdb-worker-1': {")
    print("[ERROR]       'client_id': 'CLIENT_ID',")
    print("[ERROR]       'client_secret': 'CLIENT_SECRET'")
    print("[ERROR]     }")
    print("[ERROR]   }")
    print("[ERROR]   mongo_url = mongodb://USER:PASS@localhost:27017/")
    print("[ERROR]")
    print("[ERROR] To redeem IDs, check https://develop.battle.net/access/")
    sys.exit(1)

debug = False

client = pymongo.MongoClient(tokens.mongo_url)
covdb = client['covdb']

def export_realms(db_characters, region):
    print("[INFO] Export realms {region}".format(region=region))
    realms = db_characters.distinct('realm')
    with open('{path}/CovDB/db/db_realms_{region}.lua'.format(path=addon_path, region=region), 'w', encoding='utf8') as f:
        f.write('local _, ns = ...\n')
        f.write('local region = "{region}"\n'.format(region=region))
        f.write('local F\n\n')
        for realm in realms:
            for faction in ["a", "h"]:
                f.write('F = function() ns.db{faction}["{realm}"]={{}} end; F()\n'.format(faction=faction[:1], realm=realm))

def export_characters(db_characters, region, faction):
    print("[INFO] Export {region}-{faction}".format(region=region, faction=faction))
    realms = db_characters.distinct('realm')
    covenantIds = {1, 2, 3, 4}
    faction_proper = faction.title()
    region_upper = region.upper()
    faction_single = faction_proper[0]
    with open('{path}/CovDB/db/db_characters_{region}_{faction}.lua'.format(path=addon_path, region=region, faction=faction), 'w', encoding='utf8') as f:
        f.write('--DB Version: {date}\n'.format(addon_version=addon_version,date=datetime.datetime.today().strftime('%Y%m%d')))
        f.write('local _, ns = ...\n')
        f.write('local region = "{region}"\n'.format(region=region))
        f.write('local F\n\n')
        f.write('local function Load(self, event, ...)\n')
        for realm in realms:
            f.write('\tF = function() ns.db{faction}["{realm}"]={{\n'.format(faction=faction[:1], realm=realm))
            for id in covenantIds:
                f.write('\t\t{\n')
                characters = db_characters.find({'realm': realm, "covenant.chosen_covenant_id":id})
                for char in characters:
                    f.write('\t\t\t"{name}",\n'.format(name=char['name']))
                f.write('\t\t},\n')
            f.write('\t} end; F()\n')
        f.write('end\n')
        f.write('local Load_Frame = CreateFrame("FRAME")\n')
        f.write('if region == ns.REGION then\n')
        f.write('    Load_Frame:RegisterEvent("PLAYER_ENTERING_WORLD")\n')
        f.write('    Load_Frame:SetScript("OnEvent", Load)\n')
        f.write('end\n')

        with open('{path}/CovDB_{region_upper}_{faction_single}/CovDB_{region_upper}_{faction_single}.toc'.format(path=addon_path, region_upper=region_upper, faction_single=faction_single), 'w', encoding='utf8') as f:
            f.write('## Interface: {interface_version}\n'.format(interface_version=interface_version))
            f.write('## Title: CovDB |cffFFFFFFCovenant DB|r ({region_upper} - {faction_proper})\n'.format(region_upper=region_upper, faction_proper=faction_proper))
            f.write('## Author: Online\n')
            f.write('## Dependencies: CovDB\n')
            f.write('## Version: {addon_version}-{date}\n'.format(addon_version=addon_version,date=datetime.datetime.today().strftime('%Y%m%d')))
            f.write('## Notes: Covenant Database for {faction_proper} characters in the {region_upper} region\n'.format(path=addon_path, region_upper=region_upper, faction_proper=faction_proper))
            f.write('\n')
            f.write('../CovDB/db/db_characters_{region}_{faction}.lua\n'.format(region=region, faction=faction))

def update_toc():
    with open('{path}/CovDB/CovDB.toc'.format(path=addon_path), 'w', encoding='utf8') as f:
        f.write('## Interface: {interface_version}\n'.format(interface_version=interface_version))
        f.write('## Title: CovDB\n')
        f.write('## Author: Online\n')
        f.write('## Version: {addon_version}\n'.format(addon_version=addon_version))
        f.write('## Notes: Show Covenant information on tooltips\n\n')

        f.write('CovDB.lua\n')
        for r in ["eu", "us", "kr", "tw"]:
        #for r in ["us"]:
            for faction in ["alliance", "horde"]:
                f.write('db/db_characters_{r}_{faction}.lua\n'.format(r=r, faction=faction))

def main():
    for r in ["eu", "us", "kr", "tw"]:
    #for r in ["us",]:
        for f in ["alliance", "horde"]:
            export_characters(covdb['characters_{r}_{f}'.format(r=r, f=f)], r, f)
    update_toc()

main()
