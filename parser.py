import json
import argparse
from collections import deque

blocks = {}
startBlockId = None

variables = {}

def runFlow(startBlockId):

    activeLines = deque([startBlockId])
    block = blocks[blockId]

    while activeLines:
        blockId = activeLines.popleft()
        end = False
        match block["type"]:
            case "terminator":
                if block["value"] == "END":
                    end = True
                pass
            case "io":
                if block["subtype"] == "input":
                    variables[blocks["variable"]] = input(blocks["value"])
                elif block["subtype"] == "output":
                    print(blocks["value"])

        if not end:
            for line in blocks.get("lines", []):
                activeLines.append(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("parser.py")
    parser.add_argument("file", help="The flow file to parse")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        flow = json.load(f)

    blocks = flow["chart"]
    for blockId, block in blocks.items():
        if block["type"] == "terminator" and block["value"] == "START":
            startBlockId = blockId
            break

    quit = False
    runFlow(startBlockId)