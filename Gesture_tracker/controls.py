def pause_or_play(sp):
    playing = sp.current_playback()

    if playing and playing.get("is_playing"):
        sp.pause_playback()
        print("Paused the music.")
    else:
        sp.start_playback()
        print("Playing the music.")


def next_track(sp):
    try:
        sp.next_track()
        print("Next track")
    except Exception as e:
        print("Couldn't skip —", e)


def previous_track(sp):
    try:
        sp.previous_track()
        print("Previous track")
    except Exception as e:
        print("Couldn't go back —", e)


def volume_up(sp):
    devices = sp.devices()
    active = next((d for d in devices['devices'] if d['is_active']), None)

    if active:
        print("Active device:", active['name'])
        print("Current volume:", active['volume_percent'])

        new_volume = min(active['volume_percent'] + 10, 100)
        sp.volume(new_volume)
        print(f"Turned volume up to {new_volume}%.")
    else:
        print("No active device found.")


def volume_down(sp):
    devices = sp.devices()
    active = next((d for d in devices['devices'] if d['is_active']), None)

    if active:
        current_vol = active['volume_percent']

        if current_vol is None or current_vol < 0 or current_vol > 100:
            print("Volume value looks off. Skipping.")
            return

        new_vol = max(current_vol - 10, 0)
        sp.volume(new_vol)
        print(f"Turned volume down to {new_vol}%.")
    else:
        print("No active device found.")


def transfer_to_desktop(sp):
    devices = sp.devices()
    for d in devices['devices']:
        if "Spotify" in d['name'] and not d['is_restricted']:
            sp.transfer_playback(device_id=d['id'], force_play=True)
            print(f"Switched playback to {d['name']}")
            return
    print("Couldn't find Spotify Desktop app.")
