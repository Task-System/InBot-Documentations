# flake8: noqa
# pylint: disable=missing-module-docstring

from pathlib import Path
from typing import cast
import xml.etree.ElementTree as ET


if __name__ == "__main__":
    # Convert every dir inside Trees to a single file
    trees = Path(__file__).parent / "Trees"
    if not trees.is_dir():
        raise FileNotFoundError(f"{trees} not found")

    build_dir = Path(__file__).parent / "Build"
    if not build_dir.is_dir():
        build_dir.mkdir()

    for tree_dir in trees.iterdir():
        if not tree_dir.is_dir():
            continue

        # Get the name of the tree
        tree_name = tree_dir.name

        # Get _Details.xml file
        details_file = tree_dir / "_Details.xml"
        if not details_file.is_file():
            raise FileNotFoundError(f"{details_file} not found")

        # read the file
        with open(details_file, "r", encoding="utf8") as _f:
            tree = ET.parse(_f)
            root = tree.getroot()

        main_element = root.find("main")
        if main_element is None:
            raise ValueError(f"{details_file} does not contain a main element")

        code = cast(str, cast(ET.Element, main_element.find("code")).text)
        base = cast(str, cast(ET.Element, main_element.find("base")).text)
        flag = cast(str, cast(ET.Element, main_element.find("flag")).text)
        name = cast(str, cast(ET.Element, main_element.find("name")).text)

        info = cast(str, cast(ET.Element, root.find("info")).text)

        # Create the file path
        tree_file = Path(__file__).parent / "Build" / f"{tree_name}.xml"

        # Create the tree
        main_tag = ET.Element(
            "menu", attrib={"code": code, "base": base, "flag": flag, "name": name}
        )

        info_tag = ET.SubElement(main_tag, "info")
        info_tag.text = info

        # Add the items
        for dirs in tree_dir.iterdir():
            for item_file in dirs.glob("*.xml"):
                print(f"Adding {item_file} from {tree_dir}")
                with open(item_file, "r", encoding="utf8") as __f:
                    item_tag = ET.parse(__f).getroot()
                    main_tag.append(item_tag)

        # Write the tree to the file
        tree_tree = ET.ElementTree(main_tag)
        tree_tree.write(tree_file, encoding="utf-8", xml_declaration=True)
