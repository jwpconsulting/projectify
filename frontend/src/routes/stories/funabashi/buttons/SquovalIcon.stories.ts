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

import { makeStorybookSelect } from "$lib-stories/storybook";
import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
import type { SquovalState, SquovalIcon as Icon } from "$lib/funabashi/types";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<SquovalIcon> = {
    component: SquovalIcon,
    argTypes: {
        icon: makeStorybookSelect<Icon>({
            // TODO rename project
            "Board": "board",
            "Team member": "teamMember",
            "Label": "label",
            "Bulk": "bulk",
            "Move": "move",
            "Filter team member": "filterTeamMember",
            "Delete": "delete",
            "Ellipsis": "ellipsis",
            "Plus": "plus",
            "Edit": "edit",
            "Dots vertical": "dotsVertical",
            "Help": "help",
        }),
        state: makeStorybookSelect<SquovalState>({
            Inactive: "inactive",
            Disabled: "disabled",
            active: "active",
        }),
    },
    args: {
        action: { kind: "button", action: console.log },
        state: "active",
        icon: "plus",
    },
};
export default meta;

type Story = StoryObj<SquovalIcon>;

export const Default: Story = {
    args: {
        active: false,
    },
};

export const Active: Story = {
    args: {
        active: true,
    },
};
