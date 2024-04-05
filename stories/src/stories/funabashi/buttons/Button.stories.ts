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
import { Plus } from "@steeze-ui/heroicons";
import type { Meta, StoryObj } from "@storybook/svelte";

import { buttonColors } from "$lib/funabashi/types";
import type { ButtonAction, ButtonStyle } from "$lib/funabashi/types";
import { makeStorybookSelect } from "$lib/storybook";

import Button from "./Button.svelte";

const style = makeStorybookSelect<ButtonStyle>({
    "Primary": {
        kind: "primary",
    },
    "Secondary": {
        kind: "secondary",
    },
    "Tertiary No Icon": {
        kind: "tertiary",
    },
    "Tertiary Icon Left": {
        kind: "tertiary",
        icon: { position: "left", icon: Plus },
    },
    "Tertiary Icon Right": {
        kind: "tertiary",
        icon: { position: "right", icon: Plus },
    },
});

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
    "Submit Disabled": {
        kind: "submit",
        disabled: true,
    },
    "Anchor": { kind: "a", href: "#" },
});

const meta: Meta<Button> = {
    component: Button,
    args: {
        label: "Behold, for I am a label",
        color: "blue",
    },
    argTypes: {
        label: {
            control: "text",
        },
        color: {
            control: "radio",
            options: buttonColors,
        },
        style,
        action,
    },
};

export default meta;

export const Primary: StoryObj = {
    args: { action: "button", style: "primary" },
};

export const Secondary: StoryObj = {
    args: { action: "button", style: "secondary" },
};

export const TertiaryNoIcon: StoryObj = {
    args: { action: "button", style: "tertiary-no-icon" },
};

export const TertiaryIconLeft: StoryObj = {
    args: { action: "button", style: "tertiary-icon-left" },
};
export const TertiaryIconRight: StoryObj = {
    args: { action: "button", style: "tertiary-icon-right" },
};
