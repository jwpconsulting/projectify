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

import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
import type {
    CircleIconIcon,
    CircleIconSize,
    ButtonAction,
} from "$lib/funabashi/types";
import { makeStorybookSelect } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const action = makeStorybookSelect<ButtonAction>({
    "Button": {
        kind: "button",
        action: () => console.log("Hello, World! I am a button."),
    },
    "Button Enabled": {
        kind: "button",
        action: () => console.log("Hello, World! I am a button."),
        disabled: false,
    },
    "Button Disabled": {
        kind: "button",
        action: () => console.log("Hello, World! I am a button."),
        disabled: true,
    },
    "Anchor": { kind: "a", href: "#" },
});

const meta: Meta<CircleIcon> = {
    component: CircleIcon,
    argTypes: {
        action: action,
        icon: makeStorybookSelect<CircleIconIcon>({
            Ellipsis: "ellipsis",
            Edit: "edit",
            Delete: "delete",
            Up: "up",
            Down: "down",
            Close: "close",
        }),
        size: makeStorybookSelect<CircleIconSize>({
            Medium: "medium",
        }),
    },
    args: {
        icon: "ellipsis",
        size: "medium",
        action: "button",
    },
};
export default meta;

type Story = StoryObj<CircleIcon>;

export const Default: Story = {};
