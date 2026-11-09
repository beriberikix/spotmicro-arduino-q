# Build cad/UnoQ_board.FCStd from Arduino's UNO Q STEP model.
# Run with freecadcmd; paths come from the UNOQ_STEP and UNOQ_OUT environment variables.
# cad/SpotUnoQ.FCStd links the imported root object, which FreeCAD names "Document".
import os

import FreeCAD
import Import

step = os.environ["UNOQ_STEP"]
out = os.environ["UNOQ_OUT"]

doc = FreeCAD.newDocument("UnoQ_board")
Import.insert(step, doc.Name)
doc.recompute()
root = doc.getObject("Document")
if root is None:
    raise SystemExit("STEP import did not produce a root object named 'Document'")
root.Label = "Arduino UNO Q"
doc.saveAs(out)
print("Saved", out)
