# MIT License
#
# Copyright (c) 2024 Iakiv Kramarenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import selene.web._elements
from selene import command, have, query
from tests import const


def test_actions_within_frame_context(session_browser):
    browser = session_browser.with_(timeout=1.0)

    # GIVEN even before opened browser

    toolbar = browser.element('.tox-toolbar__primary')
    text_area_frame = browser.element('.tox-edit-area__iframe')
    text_area_frame_context = text_area_frame.frame_context  # THEN lazy;)
    text_area = browser.element('#tinymce')

    # WHEN
    browser.open(const.TINYMCE_URL)

    # AND
    with text_area_frame_context:

        # THEN
        text_area.element('p').should(
            have.property_('innerHTML').value(
                'Hello, World!',
            )
        )

        # WHEN
        text_area.perform(command.select_all)

        # AND exiting context (switch to default)...

    # AND (outside frame context)
    toolbar.element('[aria-label=Bold]').click()

    # AND (coming back to frame context)
    with text_area_frame_context:

        # THEN
        text_area.element('p').should(
            have.property_('innerHTML').value('<strong>Hello, World!</strong>')
        )

        # WHEN (just one more example)
        text_area.perform(command.select_all).type(
            'New content',
        )

        # THEN
        text_area.element('p').should(
            have.property_('innerHTML').value(
                '<strong>New content</strong>',
            )
        )
