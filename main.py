import time
import numpy as np
import matplotlib.pyplot as plt
from arduino import Arduino

LOOP_DURATION = 30
TIME_INTERVAL = 10
BUTTON_PINS = ["a:1:i", "a:2:i", "a:3:i"]
DEBOUNCE_TIME = 0.3
PORT = "COM6"

if __name__ == '__main__':
    uno = Arduino(PORT=PORT)

    num_intervals = LOOP_DURATION // TIME_INTERVAL
    num_buttons = len(BUTTON_PINS)
    click_count = np.zeros((num_intervals, num_buttons), dtype=int)

    # For debouncing
    last_button_states = [False] * num_buttons
    last_press_times = [0] * num_buttons

    start_time = time.time()

    # --- Main Loop ---
    while time.time() - start_time < LOOP_DURATION:
        current_time = time.time()
        elapsed_time = current_time - start_time
        index = int(elapsed_time / TIME_INTERVAL)

        if index < num_intervals:
            for i, pin in enumerate(BUTTON_PINS):
                current_state = uno.is_button_press(pin)

                if current_state and not last_button_states[i] and (current_time - last_press_times[i] > DEBOUNCE_TIME):
                    click_count[index, i] += 1
                    last_press_times[i] = current_time
                    print(i, index)

                last_button_states[i] = current_state

        time.sleep(0.01)

    uno.buzzer_dot()

    mean_clicks = np.mean(click_count, axis=0)

    labels = [f"{i*10}-{(i+1)*10} 초" for i in range(num_intervals)]
    bottom = np.zeros(num_intervals)

    fig, ax = plt.subplots()

    for i in range(num_buttons):
        ax.bar(labels, click_count[:, i], label=f'핀 - {i+1}', bottom=bottom)
        bottom += click_count[:, i]

    plt.show()
