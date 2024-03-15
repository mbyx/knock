from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import Factory, define

if TYPE_CHECKING:
    from depict.canvas import Canvas
    from depict.engine import Engine


@define
class Scene:
    """The smallest unit for logic in depict.

    This object can have a tag that must be unique at the same nesting
    level. It can also have children and can be a part of multiple groups.

    While depict does not enforce the uniqueness of a tag, methods such as
    `get_node` will only return the first matching node if there is more than
    one node with the same tag."""

    tag: str = ""
    children: list[Scene] = Factory(list)
    groups: list[str] = Factory(list)
    parent: Scene | None = None

    def __attrs_post_init__(self) -> None:
        self.children = self.build()
        if not self.tag:  # If no tag has been set, default to the name of the class.
            self.tag = self.__class__.__name__

    def world(self) -> list[Scene]:
        """Get every single node in a scene, no matter how deeply nested.

        This method is recursive, and it is preferred that it is not used."""
        nodes: list[Scene] = []
        for child in self.children:
            if child.children != []:
                nodes.extend(child.world())
            nodes.append(child)
        return nodes

    def get_node(self, query: str) -> Scene | None:
        """Find a given node by searching recursively from the current scene.

        The `query` string is in the form `Parent.Child` and can be as deep
        as needed. This method cannot query sibling or parent nodes."""
        descendants: list[str] = query.split(".")
        for child in self.children:
            if child.tag == descendants[0] and len(descendants) != 1:
                node: Scene | None = child.get_node(".".join(descendants[1:]))
                return node
            elif child.tag == descendants[0] and len(descendants) == 1:
                return child

    def is_in_group(self, group: str) -> bool:
        """Determine whether a node is in a group or not."""
        return group in self.groups

    def get_nodes_in_group(self, group: str) -> list[Scene]:
        """Find all nodes that are in the same `group` recursively."""
        nodes: list[Scene] = []
        for child in self.children:
            if child.is_in_group(group):
                nodes.append(child)
            nodes.extend(child.get_nodes_in_group(group))
        return nodes

    def build(self) -> list[Scene]:
        # TODO: Combine build and ready methods into one.
        """Build the children to be attached to the node."""
        return self.children

    def draw(self, canvas: Canvas) -> None:
        """Draw the node to the canvas every clock tick."""

    def tick(self, delta: float, engine: Engine) -> None:
        """Perform logic every clock tick.

        This method provides one argument; delta. This is the time elapsed
        since `tick` was last called."""

    def ready(self, engine: Engine) -> None:
        """Called once, as soon as depict is initialized."""
