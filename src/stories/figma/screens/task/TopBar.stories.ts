import type { Meta, StoryObj } from "@storybook/svelte";

import TopBar from "$lib/figma/screens/task/TopBar.svelte";

const meta: Meta<TopBar> = {
    component: TopBar,
    argTypes: {},
};
export default meta;

type Story = StoryObj<TopBar>;

export const Default: Story = {};
