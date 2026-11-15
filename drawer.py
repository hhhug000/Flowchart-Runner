import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from PIL import ImageDraw

if not hasattr(ImageDraw.ImageDraw, "textsize"):
    def _textsize(self, text, font=None, *args, **kwargs):
        bbox = self.textbbox((0, 0), text, font=font)
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])
    ImageDraw.ImageDraw.textsize = _textsize

from blockdiag import parser, builder, drawer

def drawFlow(flow, outputName="flowchart"):
    blocks = flow["chart"]

    diag_lines = ["blockdiag {"]
    diag_lines.append("  default_shape = roundedbox;")

    shape_map = {
        "terminator": "flowchart.terminator",
        "io": "flowchart.input",
        "process": "box",
        "decision": "diamond",
        "subprocess": "box"
    }

    for blockId, block in blocks.items():
        b_type = block.get("type", "process")
        value = block.get("value", blockId).replace('"', '\\"')
        shape = shape_map.get(b_type, "box")

        attrs = ""
        if b_type == "subprocess":
            attrs = ', color="#e8f0fe", style="dashed"'

        diag_lines.append(f'  {blockId} [label="{value}", shape="{shape}", width=170{attrs}];')

    for blockId, block in blocks.items():
        lines = block.get("lines")
        if not lines:
            continue

        if isinstance(lines, dict):
            for condition, target in lines.items():
                diag_lines.append(f'  {blockId} -> {target} [label="{condition}"];')
        elif isinstance(lines, list):
            for target in lines:
                diag_lines.append(f'  {blockId} -> {target};')

    diag_lines.append("}")

    diag_code = "\n".join(diag_lines)

    tree = parser.parse_string(diag_code)
    diagram = builder.ScreenNodeBuilder.build(tree)

    output_file = f"{outputName}.png"
    draw = drawer.DiagramDraw('PNG', diagram, filename=output_file)
    draw.draw()
    draw.save()

    print(f"Flowchart PNG saved to {output_file}")
