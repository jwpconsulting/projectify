# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Workspace app utils."""

from typing import Optional

from django.utils.safestring import SafeString, mark_safe

from justhtml import JustHTML, PruneEmpty

from projectify.lib.settings import get_settings


def extract_first_paragraph_text(unsafe_html: str) -> Optional[str]:
    """Return plain text from the first non-empty block tag in html, or None."""
    if len(unsafe_html) == 0:
        return None
    settings = get_settings()
    doc = JustHTML(
        unsafe_html,
        policy=settings.HTML_USER_POLICY,
        fragment=True,
        transforms=[PruneEmpty("*")],
    )
    match doc.root.children:
        case None | []:
            return None
        case children:
            pass
    # Try extracting the contents of the first non-empty HTML element
    for child in children:
        text: str = child.to_text()
        if len(text) > 0:
            return text
    return None


def strip_first_paragraph(unsafe_html: str) -> Optional[SafeString]:
    """
    Strip the first paragraph or other block element.

    Return all following paragraphs as long they're not empty.

    Return None if there's nothing after the first block.
    """
    if len(unsafe_html) == 0:
        return None
    settings = get_settings()
    doc = JustHTML(
        unsafe_html,
        policy=settings.HTML_USER_POLICY,
        fragment=True,
        transforms=[PruneEmpty("*")],
    )
    match doc.root.children:
        case None:
            return None
        # Empty or just one element
        case [] | [_]:
            return None
        case children:
            doc.root.children = children[1:]
            sanitized_html = doc.to_html()
            # calling mark_safe doesn't make it safe
            # html is safe because JustHTML outputs safe html in
            # doc.to_html()
            return mark_safe(sanitized_html)
