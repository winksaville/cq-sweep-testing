import sys

import cadquery as cq  # type: ignore

if "cq_editor" in sys.modules:

    from __main__ import self

    def show(o: cq.Workplane, name=None) -> None:
        # self.components["object_tree"].addObject(o)
        show_object(o, name=name)


else:

    def show(o: cq.Workplane, name=None):
        if name is None:
            name = str(id(o))
        print(f"{name}={vars(o)}")


def updatePendingWires(wp: cq.Workplane) -> cq.Workplane:
    """Fix cq bug https://github.com/CadQuery/cadquery/issues/421"""
    wp.ctx.pendingWires = []
    return wp.each(lambda shape: shape)


# The path that we'll sweep
path = cq.Workplane("XZ").moveTo(0, 4).radiusArc(endPoint=(4, 0), radius=4)
# show(path, name="path")

# Sketch 1
s1 = cq.Workplane("YZ").moveTo(0, 4).rect(2, 1)
# show(s1, name="s1")

# Sketch 2
s2 = cq.Workplane("XY").moveTo(4, 0).circle(0.5)
# show(s2, name="s2")
#
# Update pending wires to fix bug
c = updatePendingWires(s1.add(s2))
# print(f"len(c.ctx.pendingWires)={len(c.ctx.pendingWires)}")
# show(c, name="c")

# This the desired output, only the rectangle in s1 was used in the sweep
result = c.sweep(path, multisection=True).translate((0, 0, 0))
show(result, name="result")
