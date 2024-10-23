// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

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
