#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et
import ctypes
import sys
import tokenize
import webbrowser
import pyperclip as pc
import kociemba
import argparse
from video import webcam
import i18n
import os
from config import config
from constants import (
    ROOT_DIR,
    E_INCORRECTLY_SCANNED,
    E_ALREADY_SOLVED
)

# Set default locale.
locale = config.get_setting('locale')
if not locale:
    config.set_setting('locale', 'en')
    locale = config.get_setting('locale')

# Init i18n.
i18n.load_path.append(os.path.join(ROOT_DIR, 'translations'))
i18n.set('filename_format', '{locale}.{format}')
i18n.set('file_format', 'json')
i18n.set('locale', locale)
i18n.set('fallback', 'en')


class Qbr:

    def __init__(self, normalize):
        self.normalize = normalize

    def run(self):
        """The main function that will run the Qbr program."""
        state = webcam.run()

        # If we receive a number then it's an error code.
        if isinstance(state, int) and state > 0:
            self.print_E_and_exit(state)

        try:
            algorithm = kociemba.solve(state)
            length = len(algorithm.split(' '))

        except Exception:
           self.print_E_and_exit(E_INCORRECTLY_SCANNED)

        print(i18n.t('startingPosition'))
        print(i18n.t('moves', moves=length))
        print(i18n.t('solution', algorithm=algorithm))
        print(state)

        scramble_alg = "0"
        state = state.replace("U", "1") #0 223113223 626626626 334336334 111444111 255155255 445665445
        state = state.replace("R", "4") #0 223113223 445665445 334336334 255155255 111444111626626626
        state = state.replace("F", "3")
        state = state.replace("D", "6")
        state = state.replace("L", "2")
        state = state.replace("B", "5")

        n = 9
        chunks = [state[i:i + n] for i in range(0, len(state), n)]
        print(chunks)

        scramble_alg += chunks[0]
        scramble_alg += chunks[4]
        scramble_alg += chunks[2]
        scramble_alg += chunks[1]
        scramble_alg += chunks[5]
        scramble_alg += chunks[3]

        print(scramble_alg)

        web_url = "https://rubiks-cube-solver.com/solution.php?cube=" + scramble_alg

        webbrowser.open(web_url)
#        reversing_algo = algorithm
#        scramble_array = reversing_algo.split()
#        print(scramble_array)
#        scramble_array_reversed = scramble_array[::-1]
#        print(scramble_array_reversed)

#        for i in range(len(scramble_array_reversed)):
#            if '\'' in scramble_array_reversed[i]:
#                scramble_array_reversed[i] = scramble_array_reversed[i].replace('\'', '', 1)
#            else:
#                scramble_array_reversed[i] += '\''
#
#        print(scramble_array_reversed)
#        scramble_algo = ' '.join(scramble_array_reversed)
#        pc.copy(scramble_algo)
#        print(i18n.t(scramble_algo))

        if self.normalize:
            for index, notation in enumerate(algorithm.split(' ')):
                text = i18n.t('solveManual.{}'.format(notation))
                print('{}. {}'.format(index + 1, text))

    def print_E_and_exit(self, code):
        """Print an error message based on the code and exit the program."""
        if code == E_INCORRECTLY_SCANNED:
            print('\033[0;33m[{}] {}'.format(i18n.t('error'), i18n.t('haventScannedAllSides')))
            print('{}\033[0m'.format(i18n.t('pleaseTryAgain')))
            body_Str = "Not all sides scanned or incorrectly scanned. Please try Again."

            title_Str = "Error"

            os.system("osascript -e \'Tell application \"System Events\" to display dialog \""+body_Str+"\" with title \""+title_Str+"\"\'")

        elif code == E_ALREADY_SOLVED:
            print('\033[0;33m[{}] {}'.format(i18n.t('error'), i18n.t('cubeAlreadySolved')))
            body_Str = "Cube is already solved"

            title_Str = "Title"

            os.system("osascript -e \'Tell application \"System Events\" to display dialog \""+body_Str+"\" with title \""+title_Str+"\"\'")
        sys.exit(code)


if __name__ == '__main__':
    # Define the application arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        '--normalize',
        default=False,
        action='store_true',
        help='Shows the solution normalized. For example "R2" would be: \
              "Turn the right side 180 degrees".'
    )
    args = parser.parse_args()

    # Run Qbr with all arguments.
    Qbr(args.normalize).run()
