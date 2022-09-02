from OCP.gp import gp_Trsf, gp_XYZ
from cadquery import Solid, Workplane
from locatable import LocatableMixin


class FilletBox(LocatableMixin):
    def __init__(
        self,
        length: float,
        width: float,
        height: float,
        radius: float,
        xform: gp_Trsf = gp_Trsf(),
    ):
        self.length = length
        self.width = width
        self.height = height
        self.radius = radius
        # Don't have to use gp_Trsf for transforms, but using it here
        # as it's conveniently available and I sort of understand it.
        self.xform = xform

    def __cadquery_solid__(self) -> Solid:
        obj = Solid.makeBox(self.length, self.width, self.height)
        obj_edges = obj.Edges()
        fobj: Solid = obj.fillet(self.radius, obj_edges)
        # XXX - Use of private Solid._apply_transform() but can
        # avoided easily by starting with self.xform and calling the
        # Solid.scale(), Solid.rotate(), and Solid.translate().  Or
        # Solid could have a public way of accepting a gp_Trsf.
        return fobj._apply_transform(self.xform)

    def _apply_transform(self, Tr: gp_Trsf) -> "FilletBox":
        return FilletBox(
            self.length,
            self.width,
            self.height,
            self.radius,
            self.xform * Tr,
        )

    def scale(self, factor: float) -> "FilletBox":
        """
        Scale this shape, but only if it hasn't been translated

        Suppose you wanted an object that cannot be scaled (for
        example, maybe it doesn't make sense to scale an M6 nut).
        This is where you would forbid the user.

        Here I've done something sillier which is to forbid scaling if
        the object has been translated.  Just a demonstration of where
        customizations would go.

        """
        trans: gp_XYZ = self.xform.TranslationPart()
        if (trans.X(), trans.Y(), trans.Z()) != (0, 0, 0):
            raise Exception("cannot scale a translated object")
        return FilletBox(
            self.length * factor,
            self.width * factor,
            self.height * factor,
            self.radius * factor,
            self.xform,
        )


fillet_box = FilletBox(length=10, width=8, height=5, radius=1)

print(f"{fillet_box=}")
print(f"{fillet_box.translate((1, 2, 3))=}")
print(f"{fillet_box.scale(2)=}")
print(f"{Solid(fillet_box)=}")
print(f"{Workplane().union(fillet_box).findSolid()=}")


from cadquery.cq import SolidLike  # not usually needed

print(f"{isinstance(fillet_box, SolidLike)=}")
print(f"{isinstance(Solid.makeBox(3,4,5), SolidLike)=}")
