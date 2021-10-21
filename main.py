import os.path
from utils import *

if __name__ == "__main__":
    file_root = './'  # the folder of your xml file
    file_name = r"_map_BPM=RT_H.xml"
    output_file_name = r"tmp_1.xml"
    # read xml file under selected folder
    test_tree = read_xml(os.path.join(file_root, file_name))
    # check errors in HOLD and SUB notes
    check(test_tree)

    # An Example
    # Demand: copy (or move, you need to manually copy the original notes to output xml file)
    #         bottom (mirrored) and left notes from time 30-40 to time 90-100
    # Preparation: make sure that no bottom and left notes at time 90-100
    t_part = [30, 40]
    t_destination = 90
    # 1.find notes from the both sides
    nodes_b = test_tree.findall(f"{bottom}/CMapNoteAsset")
    nodes_l = test_tree.findall(f"{left}/CMapNoteAsset")
    # 2.find notes from both sides where note time between 30 and 40
    nodes_b_part = [node for node in nodes_b if is_in_range(node, 'm_time', t_part[0], t_part[1])]
    nodes_l_part = [node for node in nodes_l if is_in_range(node, 'm_time', t_part[0], t_part[1])]
    # 3.delay these notes by time 90-30
    nodes_b_time = [node[attr_dict['m_time']] for node in nodes_b_part]
    nodes_l_time = [node[attr_dict['m_time']] for node in nodes_l_part]
    t_delay = t_destination - t_part[0]
    delay_node_text(nodes_b_time, t_delay)
    delay_node_text(nodes_l_time, t_delay)
    # 4.mirror bottom notes
    nodes_b_pos = [node[attr_dict['m_position']] for node in nodes_b_part]
    nodes_b_size = [node[attr_dict['m_width']] for node in nodes_b_part]
    mirror_node_pos(nodes_b_pos, nodes_b_size)
    # 5.get ids of notes at time 30-40 and 90-100
    b_part_start_id = int(nodes_b_part[0][attr_dict['m_id']].text)
    b_part_end_id = b_part_start_id + len(nodes_b_part) - 1
    l_part_start_id = int(nodes_l_part[0][attr_dict['m_id']].text)
    l_part_end_id = l_part_start_id + len(nodes_l_part) - 1
    print(f"original bottom part's id range: [{b_part_start_id}, {b_part_end_id}]")
    print(f"original left part's id range: [{l_part_start_id}, {l_part_end_id}]")
    nodes_b_mid = [node for node in nodes_b if is_in_range(node, 'm_time', 60.001, 90)]
    nodes_l_mid = [node for node in nodes_l if is_in_range(node, 'm_time', 60.001, 90)]
    # 6.delay selected notes by id
    b_part_id_delay = len(nodes_b_part) + len(nodes_b_mid)
    l_part_id_delay = len(nodes_l_part) + len(nodes_l_mid)
    print(f"original bottom part's id should be delayed by {b_part_id_delay}")
    print(f"original left part's id should be delayed by {l_part_id_delay}")
    nodes_b_part_id = [node[attr_dict['m_id']] for node in nodes_b_part]
    nodes_b_part_id += [node[attr_dict['m_subId']] for node in nodes_b_part]
    nodes_l_part_id = [node[attr_dict['m_id']] for node in nodes_l_part]
    nodes_l_part_id += [node[attr_dict['m_subId']] for node in nodes_l_part]
    delay_node_text(nodes_b_part_id, b_part_id_delay)
    delay_node_text(nodes_l_part_id, l_part_id_delay)
    # 7.delay notes after time 90 by id
    nodes_b_destination = [node for node in nodes_b if is_in_range(node, 'm_time', min=90)]
    nodes_l_destination = [node for node in nodes_l if is_in_range(node, 'm_time', min=90)]
    b_destination_id_delay = len(nodes_b_part)
    l_destination_id_delay = len(nodes_l_part)
    nodes_b_destination_id = [node[attr_dict['m_id']] for node in nodes_b_destination]
    nodes_b_destination_id += [node[attr_dict['m_subId']] for node in nodes_b_destination]
    nodes_l_destination_id = [node[attr_dict['m_id']] for node in nodes_l_destination]
    nodes_l_destination_id += [node[attr_dict['m_subId']] for node in nodes_l_destination]
    delay_node_text(nodes_b_destination_id, b_destination_id_delay)
    delay_node_text(nodes_l_destination_id, l_destination_id_delay)

    # save new xml file
    write_xml(test_tree, os.path.join(file_root, output_file_name))