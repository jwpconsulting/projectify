// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
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
import type { Meta, StoryObj } from "@storybook/svelte";

import Breadcrumbs from "$lib/figma/screens/task/Breadcrumbs.svelte";
import { makeStorybookSelect } from "$lib/storybook";

// TODO
const choices = {
    "All links": [
        { label: "This is a label, it is long, and informative", href: "#" },
        {
            label: "This here is a label, it is long, and informative",
            href: "#",
        },
        { label: "This too a label, it is long, and informative", href: "#" },
        {
            label: "Now, this is a label, it is long, and informative",
            href: "#",
        },
    ],
    "A few labels": [
        { label: "This is a label, it is long, and informative", href: "#" },
        { label: "This here is a label, it is long, and informative" },
        { label: "This too a label, it is long, and informative", href: "#" },
        { label: "Now, this is a label, it is long, and informative" },
        { label: "The revolution will not be televised" },
    ],
    // Add more labels, wayyyyy more XXX
    "Only labels": [
        { label: "I am a label" },
        { label: "I too am a label" },
        { label: "Plug in, turn on, and cop out" },
        { label: "lowercase on purpose, hello, I am a crumb" },
        { label: "Applepie crumb" },
        { label: "Crumblicious" },
    ],
    "Empty": [],
};

const meta: Meta<Breadcrumbs> = {
    component: Breadcrumbs,
    argTypes: {
        crumbs: makeStorybookSelect(choices),
    },
};
export default meta;

type Story = StoryObj<Breadcrumbs>;

export const Default: Story = {
    args: { crumbs: "all-links" },
};

export const AFewLabels: Story = {
    args: { crumbs: "a-few-labels" },
};

export const OnlyLabels: Story = {
    args: { crumbs: "only-labels" },
};

export const Empty: Story = {
    args: { crumbs: "empty" },
};
