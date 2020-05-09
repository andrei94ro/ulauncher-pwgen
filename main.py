"""
Ulauncher PWGen extension.
Generates strong passwords using pwgen tool.
"""
import logging
from subprocess import check_output
from os import path, access, environ, pathsep, X_OK
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from random import SystemRandom

choice = SystemRandom().choice

LOGGER = logging.getLogger(__name__)


def is_exist(program):
    """ Checks if the pwgen cli is installed in the system """

    def is_exe(fpath):
        return path.isfile(fpath) and access(fpath, X_OK)

    fpath, _ = path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for mypath in environ["PATH"].split(pathsep):
            exe_file = path.join(mypath, program)
            if is_exe(exe_file):
                return exe_file

    return None


class PwgenExtension(Extension):
    """ Main Extension Constructor """

    def __init__(self):
        LOGGER.info('init Pwgen Extension')
        super(PwgenExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    """ Class that listens to the Keyboard event """

    def on_event(self, event, extension):
        """ Handles event """
        items = []

        if event.get_argument():
            pw_length = int(event.get_argument())
        else:
            pw_length = int(extension.preferences['pw_length'])

        pw_count = int(extension.preferences['pw_count'])

        passwords = self.generatePasswords(
            pw_length,
            pw_count,
        )

        for password in passwords:
            items.append(
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=str(password),
                    description='Press Enter to copy this password to clipboard',
                    highlightable=False,
                    on_enter=CopyToClipboardAction(str(password))
                )
            )

        return RenderResultListAction(items)

    def generatePasswords(self, length, count):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!$%&()*+,-./:;=?@[]^_`{|}~'
        passwords = []
        while len(passwords) < int(count):
            password = "".join(choice(chars) for x in range(length))
            passwords.append(password)

        if len(passwords) == 1:
            return passwords[0]

        return passwords


if __name__ == '__main__':
    PwgenExtension().run()
