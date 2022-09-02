from OCP.gp import gp_Pnt, gp_Trsf
from cadquery import Vector
from cadquery.occ_impl.geom import VectorLike
from typing import Protocol, TypeVar


T = TypeVar("T")
TLocatable = TypeVar("TLocatable", bound="Locatable")


class Locatable(Protocol):

    """A class that implements this protocol (i.e. implements the below
    method) can be used with LocatableMixin

    """

    def _apply_transform(self: TLocatable, Tr: gp_Trsf) -> TLocatable:
        """
        Make a copy of the current object with `Tr` applied

        """
        ...


class LocatableMixin:

    """
    Mixin for adding methods for changing location

    These are currently just copied from Solid, but they could (or
    should?)  written in be written some OCP-independent way.

    Solid-like objects that want to be locatable can inherit this
    mixin and implement `_apply_transform()`.  Or they are free to
    implement any rotate, translate, and scale methods they want.

    """

    def translate(self: TLocatable, vector: VectorLike) -> TLocatable:
        """
        Translates this shape through a transformation.
        """

        T = gp_Trsf()
        T.SetTranslation(Vector(vector).wrapped)

        return self._apply_transform(T)

    def scale(self: TLocatable, factor: float) -> TLocatable:
        """
        Scales this shape through a transformation.
        """

        T = gp_Trsf()
        T.SetScale(gp_Pnt(), factor)

        return self._apply_transform(T)
