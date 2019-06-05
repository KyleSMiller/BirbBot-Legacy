from BabyBirbBot.ServerQuerier import ServerQuerier

import json
import time


def queryServers():
    """
    Query all servers provided in the .json constructor file
    Write data that is gathered to a separate .json file
    """
    servers = []

    with open("./resources/ServerConstructorInfo.json") as jsonFile:
        data = json.load(jsonFile)
        for server in data["Server Constructors"]:
            servers.append(ServerQuerier(server["Address"], server["Name"], server["IP"]))

    for server in servers:
        server.getAll()


def main():
    startTime = time.time()
    # 2 minute timer
    while True:
        currentTime = time.time()
        if currentTime == startTime + 120:
            startTime = currentTime
            queryServers()