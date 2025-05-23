// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Checkbox> = {
    component: Checkbox,
    argTypes: {
        contained: {
            control: "boolean",
        },
        checked: {
            control: "boolean",
        },
        disabled: {
            control: "boolean",
        },
    },
    args: {
        checked: false,
        contained: false,
        disabled: false,
    },
};
export default meta;

type Story = StoryObj<Checkbox>;

export const Default: Story = {};

export const DisabledChecked: Story = {
    args: { checked: true, disabled: true },
};

export const DisabledUnchecked: Story = {
    args: { checked: false, disabled: true },
};
