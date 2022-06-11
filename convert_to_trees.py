# flake8: noqa
# pylint: disable=missing-module-docstring

from pathlib import Path
from typing import cast
import xml.etree.ElementTree as ET


if __name__ == "__main__":
    built_path = Path(__file__).parent / "Build"
    if not built_path.is_dir():
        raise FileNotFoundError(f"{built_path} not found")

    output_base = Path(__file__).parent / "Trees"

    if not output_base.is_dir():
        output_base.mkdir()

    for xml_file in built_path.glob("*.xml"):

        sub_dir = output_base / xml_file.stem
        if not sub_dir.is_dir():
            sub_dir.mkdir()

        with open(xml_file, "r", encoding="utf8") as _f:
            tree = ET.parse(_f)
            root = tree.getroot()

            # Generating _Details.xml
            details_file = sub_dir / "_Details.xml"

            details_tag = ET.Element("details")
            main_element = ET.SubElement(details_tag, "main")

            c = ET.SubElement(main_element, "code")
            c.text = root.attrib["code"]
            b = ET.SubElement(main_element, "base")
            b.text = root.attrib["base"]
            f = ET.SubElement(main_element, "flag")
            f.text = root.attrib["flag"]
            f = ET.SubElement(main_element, "name")
            f.text = root.attrib["name"]

            i = ET.SubElement(details_tag, "info")
            i.text = cast(ET.Element, root.find("info")).text

            new_tree = ET.ElementTree(details_tag)
            new_tree.write(details_file, encoding="utf-8", xml_declaration=False)

            temp_data: dict[str, dict[str, ET.Element]] = {}

            # get all items in the root
            for item in root.findall("item"):
                # get item code
                item_code = item.attrib["code"]

                # check if item code ends with a number (e.g. "test_1")
                try:
                    ending = int(item_code.split("_")[-1])
                    item_code = str.join(  # pylint: disable=invalid-name
                        "_", item_code.split("_")[:-1]
                    )
                    item_name = cast(str, cast(ET.Element, item.find("btntext")).text)

                    # check if item code is already in temp_data
                    if item_code in temp_data:
                        temp_data[item_code][item_name] = item
                    else:
                        temp_data[item_code] = {item_name: item}

                except ValueError:
                    item_name = cast(str, cast(ET.Element, item.find("btntext")).text)
                    temp_data[item_code] = {item_name: item}

            for data_name, data_items in temp_data.items():
                data_dir = sub_dir / data_name
                if not data_dir.is_dir():
                    data_dir.mkdir()

                for data_item, element in data_items.items():
                    data_item_path = data_dir / (data_item.replace("\n", "") + ".xml")
                    root_element = ET.ElementTree(element)
                    root_element.write(
                        data_item_path, encoding="utf8", xml_declaration=False
                    )
