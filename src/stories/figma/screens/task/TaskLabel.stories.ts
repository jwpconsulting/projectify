import type { Meta, StoryObj } from "@storybook/svelte";

import { makeStorybookSelect, mappedLabels } from "$lib/storybook";

import TaskLabel from "$lib/figma/screens/task/TaskLabel.svelte";
import type { Label } from "$lib/types/workspace";

const meta: Meta<TaskLabel> = {
    component: TaskLabel,
    argTypes: {
        labels: makeStorybookSelect<Label[]>({
            "0 labels selected": [],
            "1 labels selected": mappedLabels.slice(0, 1),
            "3 labels selected": mappedLabels.slice(1, 4),
        }),
    },
    args: {
        // XXX I can't specify 3-labels-selected here. Would be cool if I could
        labels: mappedLabels.slice(1, 4),
    },
};
export default meta;

type Story = StoryObj<TaskLabel>;

export const Default: Story = {};

export const ApplyLabel: Story = {
    args: {
        labels: [],
    },
};
