# SPDX-License-Identifier: GPL-3.0-only

import time
import signal
import ctypes
import os
import subprocess
import argparse
from enum import Enum, auto
from .do_break import do_break


def main():
    parser = argparse.ArgumentParser(description="""Reminds you to take wrist breaks, which
    should help you prevent or manage a repetitive stress injury.""")
    parser.add_argument("max_active_time", type=int,
                        help="Max amount of time typing without a break (seconds)")
    parser.add_argument("break_time", type=int,
                        help="How long are the breaks (seconds)")
    parser.add_argument("--force-break", action="store_true",
                        help="Reopen break window if closed")
    parser.add_argument("--break-penalty", type=int, default=-1,
                        help="Seconds to add on to break if the user continues to work")
    args = parser.parse_args()

    class State(Enum):
        ACTIVE = auto()
        IDLE = auto()

    def set_pdeathsig():
        libc = ctypes.CDLL("libc.so.6")
        return libc.prctl(1, signal.SIGKILL) #1 is PR_SET_PDEATHSIG

    sigset = set((signal.SIGUSR1, signal.SIGUSR2))
    for sig in sigset:
        signal.signal(sig, lambda x, y: None)

    pid = os.getpid()
    subprocess.Popen(['swayidle', 'timeout', '1', 'kill -USR1 %s' % pid,
                      'resume', 'kill -USR2 %s' % pid],
                     preexec_fn=set_pdeathsig)

    state = State.ACTIVE
    active_time_left = args.max_active_time
    while True:
        startt = time.monotonic()
        s = signal.sigtimedwait(sigset,
                                active_time_left if state == State.ACTIVE else 86400)
        sleept = time.monotonic() - startt

        if s is None: #Timeout
            if state == State.IDLE: #Idle long enough to reset
                #XXX Track idle time instead of asserting sigtimedwait never returns early?
                assert(sleept >= args.break_time)
                active_time_left = args.max_active_time
            else: #Out of active time
                active_time_left -= sleept
        elif s.si_signo == signal.SIGUSR1: #->Idle
            assert(state == State.ACTIVE)
            active_time_left -= sleept
            state = State.IDLE
        elif s.si_signo == signal.SIGUSR2: #->Active
            assert(state == State.IDLE)
            if sleept >= args.break_time: #Idle long enough to reset.
                active_time_left = args.max_active_time
            else: #Short idle time, doesn't count as a break.
                active_time_left -= sleept
            state = State.ACTIVE

        if active_time_left < 0:
            do_break(args.break_time, args.force_break, args.break_penalty)
            active_time_left = args.max_active_time
            state = State.ACTIVE
