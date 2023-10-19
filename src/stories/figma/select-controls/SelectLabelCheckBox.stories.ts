import type { Meta, StoryObj } from "@storybook/svelte";

import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
import type { SelectLabel } from "$lib/figma/types";
import { makeStorybookSelect, selectLabels } from "$lib/storybook";

const label = makeStorybookSelect(
    Object.fromEntries(
        selectLabels.map((l, i): [string, SelectLabel] => [i.toString(), l])
    )
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
