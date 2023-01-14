from knock.depict.scene import Scene


def test_scene_init() -> None:
    scene: Scene = Scene("Custom Scene", children=[], groups=[])
    assert scene.tag == "Custom Scene"
    assert scene.children == []
    assert scene.groups == []


def test_scene_auto_tagging() -> None:
    class CustomScene(Scene):
        pass

    assert CustomScene().tag == "CustomScene"


def test_world() -> None:
    scene = Scene(
        "Father",
        children=[Scene("Son"), Scene("Daughter", children=[Scene("GrandSon")])],
    )
    nodes: list[Scene] = scene.world()
    assert len(nodes) == 3
    assert Scene("Son") in nodes
    assert Scene("Daughter", children=[Scene("GrandSon")]) in nodes
    assert Scene("GrandSon") in nodes


def test_get_node() -> None:
    scene = Scene(
        "Father",
        children=[Scene("Son"), Scene("Daughter", children=[Scene("GrandSon")])],
    )
    son: Scene | None = scene.get_node("Son")
    assert son is not None and son.tag == "Son"
    grandson: Scene | None = scene.get_node("Daughter.GrandSon")
    assert grandson is not None and grandson.tag == "GrandSon"


def test_is_in_group() -> None:
    scene = Scene("Help Me", groups=["Lonely"])
    assert scene.is_in_group("Lonely")


def test_get_nodes_in_group() -> None:
    scene = Scene(
        "Family",
        children=[
            Scene("Max", groups=["Dead"]),
            Scene("Ella", groups=["Dead"]),
            Scene("Beatrice", children=[Scene("Me", groups=["Dead"])]),
        ],
    )
    nodes: list[Scene] = scene.get_nodes_in_group("Dead")
    assert len(nodes) == 3
    assert Scene("Max", groups=["Dead"]) in nodes
    assert Scene("Ella", groups=["Dead"]) in nodes
    assert Scene("Me", groups=["Dead"]) in nodes
