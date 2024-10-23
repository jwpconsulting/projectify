// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
import type { SelectLabel } from "$lib/figma/types";
import { makeStorybookSelect, selectLabels } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const label = makeStorybookSelect(
    Object.fromEntries(
        selectLabels.map((l, i): [string, SelectLabel] => [i.toString(), l]),
    ),
);

const meta: Meta<SelectLabelCheckBox> = {
    component: SelectLabelCheckBox,
    argTypes: {
        label,
        name: { control: "text" },
        checked: { control: "boolean" },
    },
    args: {
        label: "1",
        name: "form-element-name",
        checked: false,
    },
};
export default meta;

type Story = StoryObj<SelectLabelCheckBox>;

export const Default: Story = {};
