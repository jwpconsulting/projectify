import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdateLabel from "$lib/figma/screens/task/TaskUpdateLabel.svelte";
import { mobileParameters, mappedLabels } from "$lib/storybook";

const labelChoices = [[], mappedLabels.slice(0, 1), mappedLabels.slice(0, 3)];

const meta: Meta<TaskUpdateLabel> = {
    component: TaskUpdateLabel,
    argTypes: {
        labels: {
            options: [0, 1, 2],
            mapping: labelChoices,
            control: {
                type: "radio",
                labels: {
                    0: "0 labels selected",
                    1: "1 labels selected",
                    2: "3 labels selected",
                },
            },
        },
    },
};
export default meta;

type Story = StoryObj<TaskUpdateLabel>;

export const Default: Story = {
    args: {
        labels: labelChoices[1],
    },
};

export const ApplyLabel: Story = {
    args: {
        labels: [],
    },
};
