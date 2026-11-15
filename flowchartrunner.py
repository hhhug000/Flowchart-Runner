import json
import argparse
from collections import deque
from drawer import drawFlow

blocks = {}
startBlockId = None

variables = {}

def findTerminator(label):
    for blockId, block in blocks.items():
        if block.get("type") == "terminator" and block.get("value") == label:
            return blockId
    raise ValueError(f"Terminator {label} not found")

def runFlow(startBlockId):

    activeLines = deque([startBlockId])
    callStack = []
    blockId = startBlockId

    while activeLines:
        nextBlocks = []
        blockId = activeLines.popleft()
        block = blocks[blockId]
        end = False
        match block["type"]:
            case "terminator":
                if block["value"] == "END":
                    end = True
                    if callStack:
                        for line in callStack.pop():
                            activeLines.append(line)
                pass
            case "io":
                if block["subtype"] == "input":
                    inputval = input(block["value"])
                    if block.get("datatype"):
                        match block["datatype"]:
                            case "string":
                                pass
                            case "int":
                                inputval = int(inputval)
                            case "float":
                                inputval = float(inputval)
                            case "bool":
                                inputval = bool(inputval)
                    variables[block["variable"]] = inputval
                elif block["subtype"] == "output":
                    print(block["value"].format(**variables))
            case "process":
                exec(block["value"], {}, variables)
            case "decision":
                result = str(eval(block["value"], {}, variables))
                branch = block["lines"].get(result)
                if branch:
                    if isinstance(branch, list):
                        nextBlocks = branch
                    else:
                        nextBlocks = [branch]
            case "subprocess":
                callStack.append(block.get("lines", []))
                nextBlocks = [findTerminator(block["value"])]

        if not end:
            if block["type"] not in ("decision", "subprocess"):
                nextBlocks = block.get("lines", [])

            for line in nextBlocks:
                activeLines.append(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("flowchartrunner.py")
    parser.add_argument("mode", help="The mode to run in (either run or draw)")
    parser.add_argument("file", help="The flow file to parse")
    parser.add_argument(
        "-o",
        "--output",
        default="flowchart",
        help="Output filename for draw mode (excluding extension)"
    )
    args = parser.parse_args()

    with open(args.file, "r") as f:
        flow = json.load(f)

    blocks = flow["chart"]
    for blockId, block in blocks.items():
        if block["type"] == "terminator" and block["value"] == "START":
            startBlockId = blockId
            break

    if args.mode.lower() == "run":
        runFlow(startBlockId)
    elif args.mode.lower() == "draw":
        drawFlow(flow, args.output)
    else:
        print("Invalid mode (must be either run or draw)")