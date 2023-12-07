import type { Meta, StoryObj } from "@storybook/svelte";

import BorderedIcon from "$lib/figma/buttons/BorderedIcon.svelte";

const meta: Meta<BorderedIcon> = {
    component: BorderedIcon,
};
export default meta;

type Story = StoryObj<BorderedIcon>;

export const Workspace: Story = {
    args: { type: "workspace" },
};

export const Filter: Story = {
    args: { type: "filter" },
};
