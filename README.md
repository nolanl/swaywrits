# swaywrits

swaywrits is a RSI break reminder in the spirit of [xwrits].

## Installation

XXXTODO

## Configuration

swaywrits takes 2 command line parameters:

    swaywrits max_active_time break_time

`max_active_time` is the amount of time using the computer before a break is required, in seconds. `break_time` is the length of the subsequent break in seconds. If the computer is left unused for `break_time` seconds, that also counts as a break and resets counting of active time.

To make the break window show up on all workspaces, add the following to your sway configuration:

    for_window [app_id="swaywrits"] sticky enable

Note that swaywrits requires [swayidle], so ensure that it is installed.

[xwrits]: https://www.lcdf.org/xwrits/
[swayidle]: https://github.com/swaywm/swayidle
