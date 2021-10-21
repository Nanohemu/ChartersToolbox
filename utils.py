from xml.etree.ElementTree import ElementTree

bottom = "m_notes/m_notes"
left = "m_notesLeft/m_notes"
right = "m_notesRight/m_notes"
attr_list = ['m_id', 'm_type', 'm_time', 'm_position', 'm_width', 'm_subId', 'status']
attr_dict = {a: i for i, a in enumerate(attr_list)}
__all__ = [
    "bottom", "left", "right", "attr_dict",
    "read_xml", "write_xml", "check",
    "delay_node_text", "mirror_node_pos", "is_in_range"]


def _num_char(c):
    """
    Turn a number c to a character
    :param c: a number with type int/float/double
    :return: char(c) with precise value
    """
    c = str(c)
    if '.' not in c:
        return c
    else:
        c_parts = c.split('.')
        c_f = ''
        flag = True
        for n in c_parts[1][::-1]:
            if n == '0' and flag:
                continue
            flag = False
            c_f += n
        if not flag:
            c_f += '.'
        return c_parts[0] + c_f[::-1]


def _delay(c, d):
    """
    Move a note to d time/id later or -d time/id earlier
    :param c: note attribution (time, id or else)
    :param d: time/id delay
    :return: delayed note time
    """
    if float(c) < 0:
        return c
    if '-' in d:
        c_new = eval(c + d)
    else:
        c_new = eval(c + '+' + d)
    return _num_char(c_new)


def _mirror_pos(p, s):
    """
    Change a note's position to the mirrored place
    :param p: note position
    :param s: node size
    :return: mirrored note position
    """
    p_new = 5 - float(p) - float(s)
    return _num_char(p_new)


def _check(notes, side):
    sides = ['Bottom: ', 'Left: ', 'Right: ']
    err = []
    sub_hold = {}
    hold_sub = {}
    for note in notes:
        note_type = note[1].text
        if note_type == 'HOLD':
            id = int(note[0].text)
            subid = int(note[5].text)
            if id >= subid:
                err.append(sides[side] + f"HOLD {id} behind SUB {subid}")
            sub_hold[subid] = id
        if note_type == 'SUB':
            id = int(note[0].text)
            if id not in sub_hold.keys():
                err.append(sides[side] + f"SUB {id} without HOLD")
            else:
                hold_sub[sub_hold[id]] = id

    for subid in sub_hold.keys():
        id = sub_hold[subid]
        if id not in hold_sub.keys():
            err.append(sides[side] + f"HOLD {id} without SUB {subid}")

    return err


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
    """
    Judge if the attribution value of the given node is located in given range
    """
    assert attr in ['m_id', 'm_subId', 'm_time', 'm_position', 'm_width']
    min = -float('inf') if min is None else min
    max = float('inf') if max is None else max
    val = eval(node[attr_dict[attr]].text)
    return min <= val <= max
