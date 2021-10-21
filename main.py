import os.path
from utils import *
from xml.etree.ElementTree import ElementTree


bottom = "m_notes/m_notes"
left = "m_notesLeft/m_notes"
right = "m_notesRight/m_notes"
attr_list = ['m_id', 'm_type', 'm_time', 'm_position', 'm_width', 'm_subId', 'status']
attr_dict = {a: i for i, a in enumerate(attr_list)}


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
    bnotes = tree.findall(f"{bottom}/CMapNoteAsset")
    lnotes = tree.findall(f"{left}/CMapNoteAsset")
    rnotes = tree.findall(f"{right}/CMapNoteAsset")
    err = []
    err += _check(bnotes, 0)
    err += _check(lnotes, 1)
    err += _check(rnotes, 2)
    if not err:
        print('No Error')
    else:
        for e in err:
            print(e)


def is_in_range(node, attr, min=None, max=None):
    assert attr in ['m_id', 'm_subId', 'm_time', 'm_position', 'm_width']
    min = -float('inf') if min is None else min
    max = float('inf') if max is None else max
    val = eval(node[attr_dict[attr]].text)
    return min <= val <= max


if __name__ == "__main__":
    file_root = './'  # the folder of your xml file
    file_name = r"_map_BPM=RT_H.xml"
    output_file_name = r"tmp_1.xml"
    # read xml file under selected folder
    test_tree = read_xml(os.path.join(file_root, file_name))
    # check errors in HOLD and SUB notes
    check(test_tree)

    ### BASIC FUNCTIONS ###

    # find notes from the bottom side
    nodes_b_pos = test_tree.findall(f"{bottom}/CMapNoteAsset/m_position")
    nodes_b_id = test_tree.findall(f"{bottom}/CMapNoteAsset/m_id")
    nodes_b_id += test_tree.findall(f"{bottom}/CMapNoteAsset/m_subId")
    nodes_b_size = test_tree.findall(f"{bottom}/CMapNoteAsset/m_width")
    nodes_time = test_tree.findall(f"{bottom}/CMapNoteAsset/m_time")
    # find notes from the left side
    nodes_l_id = test_tree.findall(f"{left}/CMapNoteAsset/m_id")
    nodes_l_id += test_tree.findall(f"{left}/CMapNoteAsset/m_subId")
    nodes_time += test_tree.findall(f"{left}/CMapNoteAsset/m_time")
    # find notes from the right side
    nodes_r_id = test_tree.findall(f"{right}/CMapNoteAsset/m_id")
    nodes_r_id += test_tree.findall(f"{right}/CMapNoteAsset/m_subId")
    nodes_time += test_tree.findall(f"{right}/CMapNoteAsset/m_time")

    # get all bottom notes mirrored
    mirror_node_pos(nodes_b_pos, nodes_b_size)
    # delay all bottom notes by time 16 and id 77
    delay_node_text(nodes_time, 16)
    delay_node_text(nodes_b_id, 77)
    # delay all left notes
    delay_node_text(nodes_l_id, 167-140)
    # bring forward all right notes
    delay_node_text(nodes_r_id, 140-167)

    ### ADVANCED FUNCTIONS ###

    # find notes from the bottom side
    nodes_b = test_tree.findall(f"{bottom}/CMapNoteAsset")
    # find notes from the bottom side where note id no less than 20
    nodes_b_1 = [node for node in nodes_b if is_in_range(node, 'm_id', 20)]
    # delay these notes by id 77
    nodes_b_1_id = [node[attr_dict['m_id']] for node in nodes_b_1]
    delay_node_text(nodes_b_1_id, 77)

    # find notes from the bottom side where note id no more than 60
    nodes_b_2 = [node for node in nodes_b if is_in_range(node, 'm_id', max=60)]
    # delay these notes by time 16
    nodes_b_2_time = [node[attr_dict['m_time']] for node in nodes_b_2]
    delay_node_text(nodes_b_2_time, 16)

    # find notes from the bottom side where note id between 20 and 60
    nodes_b_3 = [node for node in nodes_b if is_in_range(node, 'm_id', 20, 60)]

    # find notes from the bottom side where note time between 90.5 and 110
    nodes_b_4 = [node for node in nodes_b if is_in_range(node, 'm_time', 90.5, 110)]
    # get these notes mirrored
    nodes_b_4_pos = [node[attr_dict['m_position']] for node in nodes_b_4]
    nodes_b_4_size = [node[attr_dict['m_width']] for node in nodes_b_4]
    mirror_node_pos(nodes_b_4_pos, nodes_b_4_size)

    # find notes from the bottom side where note position not between 1.0 and 4.0
    nodes_b_5 = [
        node for node in nodes_b
        if is_in_range(node, 'm_position', max=0.99)
        or is_in_range(node, 'm_position', min=4.01)
    ]

    # save new xml file
    write_xml(test_tree, os.path.join(file_root, output_file_name))

