__all__ = ["_delay", "_mirror_pos", "_check"]


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
