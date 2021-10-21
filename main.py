import os.path
from utils import *
from xml.etree.ElementTree import ElementTree


def read_xml(in_path):
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def write_xml(tree, out_path):
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


def delay_node_text(nodelist, d=35):
    """
    Move a list of notes to d time/id later or -d time/id earlier
    :param nodelist: list of notes
    :param d: time/id delay
    """
    for node in nodelist:
        node.text = _delay(node.text, str(d))


def mirror_node_pos(pos_list, size_list):
    """
    Change a list of notes' positions to their mirrored places
    :param pos_list: notes' positions
    :param size_list: nodes' sizes
    """
    for i, node in enumerate(pos_list):
        node.text = _mirror_pos(node.text, size_list[i].text)


def check(tree):
    """
    Check if the xml map file has any error.
    """
    bnotes = tree.findall("m_notes/m_notes/CMapNoteAsset")
    lnotes = tree.findall("m_notesLeft/m_notes/CMapNoteAsset")
    rnotes = tree.findall("m_notesRight/m_notes/CMapNoteAsset")
    err = []
    err += _check(bnotes, 0)
    err += _check(lnotes, 1)
    err += _check(rnotes, 2)
    if not err:
        print('No Error')
    else:
        for e in err:
            print(e)


if __name__ == "__main__":
    file_root = './'  # the folder of your xml file
    file_name = "_map_Eastern Horoscope_G 2020-11-28 22_22_59.xml"
    output_file_name = "tmp_1.xml"
    # read xml file under selected folder
    test_tree = read_xml(os.path.join(file_root, file_name))
    # check errors in HOLD and SUB notes
    check(test_tree)

    # find notes from the bottom side
    nodes_b_pos = test_tree.findall("bottom/CMapNoteAsset/m_position")
    nodes_b_id = test_tree.findall("bottom/CMapNoteAsset/m_id")
    nodes_b_id += test_tree.findall("bottom/CMapNoteAsset/m_subId")
    nodes_b_size = test_tree.findall("bottom/CMapNoteAsset/m_width")
    nodes_time = test_tree.findall("bottom/CMapNoteAsset/m_time")
    # find notes from the left side
    nodes_l_id = test_tree.findall("left/CMapNoteAsset/m_id")
    nodes_l_id += test_tree.findall("left/CMapNoteAsset/m_subId")
    nodes_time += test_tree.findall("left/CMapNoteAsset/m_time")
    # find notes from the right side
    nodes_r_id = test_tree.findall("right/CMapNoteAsset/m_id")
    nodes_r_id += test_tree.findall("right/CMapNoteAsset/m_subId")
    nodes_time += test_tree.findall("right/CMapNoteAsset/m_time")

    # get all bottom notes mirrored
    mirror_node_pos(nodes_b_pos, nodes_b_size)
    # delay all bottom notes by time 16 and id 77
    delay_node_text(nodes_time, 16)
    delay_node_text(nodes_b_id, 77)
    # delay all left notes
    delay_node_text(nodes_l_id, 167-140)
    # bring forward all right notes
    delay_node_text(nodes_r_id, 140-167)

    # save new xml file
    write_xml(test_tree, os.path.join(file_root, output_file_name))
