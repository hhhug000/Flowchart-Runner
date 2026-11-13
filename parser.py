import json
import argparse

blocks = {}
startBlockId = None

variables = {}

def parseBlock(blockId):
    end = False
    match blocks[blockId]["type"]:
        case "terminator":
            if blocks[blockId]["value"] == "END":
                end = True
            pass
        case "io":
            if blocks[blockId]["subtype"] == "input":
                variables[blocks[blockId]["variable"]] = input(blocks[blockId]["value"])
            elif blocks[blockId]["subtype"] == "output":
                print(blocks[blockId]["value"])

    if not end:
        for line in blocks[blockId]["lines"]:
            parseBlock(line)

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
    parseBlock(startBlockId)