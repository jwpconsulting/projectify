// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import { marked } from "marked";
import { getHeadingList, gfmHeadingId } from "marked-gfm-heading-id";

interface Markdown {
    content: string;
    sections: {
        id: string;
        title: string;
    }[];
}

export function toMarkdown(raw: string): Markdown {
    marked.use(gfmHeadingId());
    const content: string = marked.parse(raw, { async: false }) as string;
    const sections = getHeadingList().map(({ id, text }) => {
        return {
            id: id,
            title: text,
        };
    });
    return { content: content, sections: sections };
}
