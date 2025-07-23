import ezdxf
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import matplotlib as draw
import uuid
import os

def convert_dxf_to_image(file_path: str, output_dir="images") -> str:
    # Naloži DXF dokument
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()

    # Pripravi risalni kontekst
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_axes([0, 0, 1, 1])
    ctx = draw.RenderContext(doc)
    draw.draw_layout(msp, ctx, ax)

    # Shrani sliko
    os.makedirs(output_dir, exist_ok=True)
    image_id = str(uuid.uuid4())
    output_path = os.path.join(output_dir, f"{image_id}.png")
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path  # vrne pot do slike
