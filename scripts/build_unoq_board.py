# Build cad/UnoQ_board.FCStd (or another board, such as cad/MediaCarrier_board.FCStd) from an
# Arduino STEP model. Run with freecadcmd; paths come from the UNOQ_STEP and UNOQ_OUT environment
# variables, and UNOQ_LABEL names the board. The assemblies link the imported root object (FreeCAD
# names it "Document" for the UNO Q and "PCB" for the Media Carrier).
import os

import FreeCAD
import Import

step = os.environ["UNOQ_STEP"]
out = os.environ["UNOQ_OUT"]

doc = FreeCAD.newDocument(os.path.splitext(os.path.basename(out))[0])
Import.insert(step, doc.Name)
doc.recompute()
roots = doc.RootObjects
root = doc.getObject("Document") or (roots[0] if len(roots) == 1 else None)
if root is None:
    raise SystemExit("STEP import did not produce a single root object")
root.Label = os.environ.get("UNOQ_LABEL", "Arduino UNO Q")
# Some STEP imports come in hidden when run headless, and links skip hidden children.
for o in doc.Objects:
    if o.TypeId in ("App::Part", "Part::Feature"):
        o.Visibility = True
doc.saveAs(out)
print("Saved", out)
