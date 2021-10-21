import os.path
from utils import *


def basic_functions_example(tree):
    # find notes from the bottom side
    nodes_b_pos = tree.findall(f"{bottom}/CMapNoteAsset/m_position")
    nodes_b_id = tree.findall(f"{bottom}/CMapNoteAsset/m_id")
    nodes_b_id += tree.findall(f"{bottom}/CMapNoteAsset/m_subId")
    nodes_b_size = tree.findall(f"{bottom}/CMapNoteAsset/m_width")
    nodes_time = tree.findall(f"{bottom}/CMapNoteAsset/m_time")
    # find notes from the left side
    nodes_l_id = tree.findall(f"{left}/CMapNoteAsset/m_id")
    nodes_l_id += tree.findall(f"{left}/CMapNoteAsset/m_subId")
    nodes_time += tree.findall(f"{left}/CMapNoteAsset/m_time")
    # find notes from the right side
    nodes_r_id = tree.findall(f"{right}/CMapNoteAsset/m_id")
    nodes_r_id += tree.findall(f"{right}/CMapNoteAsset/m_subId")
    nodes_time += tree.findall(f"{right}/CMapNoteAsset/m_time")

    # get all bottom notes mirrored
    mirror_node_pos(nodes_b_pos, nodes_b_size)
    # delay all bottom notes by time 16 and id 77
    delay_node_text(nodes_time, 16)
    delay_node_text(nodes_b_id, 77)
    # delay all left notes
    delay_node_text(nodes_l_id, 167 - 140)
    # bring forward all right notes
    delay_node_text(nodes_r_id, 140 - 167)


def advanced_functions_example(tree):
    # find notes from the bottom side
    nodes_b = tree.findall(f"{bottom}/CMapNoteAsset")
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


if __name__ == "__main__":
    file_root = './'  # the folder of your xml file
    file_name = r"_map_BPM=RT_H.xml"
    output_file_name = r"tmp_1.xml"
    # read xml file under selected folder
    test_tree = read_xml(os.path.join(file_root, file_name))
    # check errors in HOLD and SUB notes
    check(test_tree)

    # BASIC FUNCTIONS
    basic_functions_example(test_tree)

    # ADVANCED FUNCTIONS
    advanced_functions_example(test_tree)

