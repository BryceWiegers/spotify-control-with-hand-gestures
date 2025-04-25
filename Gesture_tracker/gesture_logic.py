def get_finger_states(hand, frame_size):
    h, w = frame_size
    tips = [4, 8, 12, 16, 20]
    fingers = []

    for i, tip in enumerate(tips):
        top = hand.landmark[tip]
        base = hand.landmark[tip - 2]

        if i == 0:
            fingers.append(top.x > base.x)
        else:
            fingers.append(top.y < base.y)

    return fingers


def detect_gesture(fingers, hand, frame_size):
    total = sum(fingers)

    if total == 0:
        return "fist"
    if total == 5:
        return "palm"

    # Only trigger pointing if ONLY the index is up
    if fingers == [False, True, False, False, False]:
        index = hand.landmark[8]
        wrist = hand.landmark[0]

        if index.x < wrist.x - 0.05:
            return "point_left"
        if index.x > wrist.x + 0.05:
            return "point_right"

    return None
