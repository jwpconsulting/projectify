// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2024 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
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
