import cv2
import mediapipe as mp
import math
from time import time
from spotify_setup import sp
from controls import pause_or_play, next_track, previous_track
from gesture_logic import get_finger_states

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

last_volume = -1
last_action_time = 0
feedback_text = ""
feedback_time = 0

track_name = ""
track_artist = ""


def get_distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def ms_to_minsec(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    return f"{minutes}:{seconds:02d}"


progress_ms = 0
last_progress_poll = 0
last_known_progress_time = 0


def update_progress():
    global progress_ms, track_duration, track_name, track_artist, last_progress_poll, last_known_progress_time
    try:
        data = sp.current_playback()
        if data and data.get("item"):
            progress_ms = data['progress_ms']
            track_duration = data['item']['duration_ms']
            track_name = data['item']['name']
            track_artist = data['item']['artists'][0]['name']
            last_known_progress_time = time()
    except:
        pass
    last_progress_poll = time()


update_progress()

cv2.namedWindow("Hand Tracker", cv2.WINDOW_NORMAL)
cv2.setWindowProperty(
    "Hand Tracker", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ok, frame = cam.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    h, w, _ = frame.shape

    RES_X, RES_Y = 2560, 1440
    frame = cv2.resize(frame, (RES_X, RES_Y))

    bar_w = int(RES_X * 0.8)
    bar_x = (RES_X - bar_w) // 2
    bar_y = RES_Y - 100

    now = time()

    if now - last_progress_poll > 1:
        update_progress()

    if progress_ms and track_duration:
        elapsed_since_last_poll = int((now - last_known_progress_time) * 1000)
        current_progress = min(
            progress_ms + elapsed_since_last_poll, track_duration)
    else:
        current_progress = 0

    vol_coords = None

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            fingers = get_finger_states(hand, (h, w))
            wrist = hand.landmark[0]
            x_pos = wrist.x

            if sum(fingers) == 0 and now - last_action_time > 1:
                if x_pos < 0.25:
                    previous_track(sp)
                    feedback_text = "<"
                    update_progress()
                elif x_pos > 0.75:
                    next_track(sp)
                    feedback_text = ">"
                    update_progress()
                elif 0.25 <= x_pos <= 0.75:
                    pause_or_play(sp)
                    feedback_text = "Play/Pause"
                last_action_time = now
                feedback_time = now

            if fingers == [True, True, False, False, False] and 0.25 <= x_pos <= 0.75:
                thumb = hand.landmark[4]
                index = hand.landmark[8]
                x1, y1 = int(thumb.x * w), int(thumb.y * h)
                x2, y2 = int(index.x * w), int(index.y * h)
                vol_coords = ((x1 + x2) // 2, (y1 + y2) // 2)

                dist = get_distance(x1, y1, x2, y2)
                min_dist = 20
                max_dist = 200
                dist = max(min(dist, max_dist), min_dist)
                volume = int((dist - min_dist) / (max_dist - min_dist) * 100)

                if abs(volume - last_volume) >= 5:
                    sp.volume(volume)
                    feedback_text = f"{volume}%"
                    feedback_time = now
                    last_volume = volume

            if fingers == [False, True, False, False, False]:
                index = hand.landmark[8]
                if index.y > 0.85:
                    if track_duration > 0:
                        seek_percent = index.x
                        seek_ms = int(track_duration * seek_percent)
                        sp.seek_track(seek_ms)
                        feedback_text = f"{ms_to_minsec(seek_ms)}"
                        feedback_time = now
                        update_progress()

    fill = int((current_progress / track_duration) * bar_w)
    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + bar_w, bar_y + 6), (100, 100, 100), -1)
    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + fill, bar_y + 6), (255, 255, 255), -1)
    cv2.putText(frame, ms_to_minsec(current_progress), (bar_x - 90,
                bar_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, ms_to_minsec(track_duration), (bar_x + bar_w +
                10, bar_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, f"{track_name} - {track_artist}", (bar_x,
                bar_y - 40), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)

    cv2.putText(frame, "<", (100, RES_Y // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    cv2.putText(frame, ">", (RES_X - 130, RES_Y // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

    if feedback_text and now - feedback_time < 2:
        if "%" in feedback_text and vol_coords:
            cv2.putText(frame, feedback_text, vol_coords,
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        elif feedback_text not in ["<", ">"]:
            cv2.putText(frame, feedback_text, (80, 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    cv2.imshow("Hand Tracker", frame)

    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break

cam.release()
cv2.destroyAllWindows()
