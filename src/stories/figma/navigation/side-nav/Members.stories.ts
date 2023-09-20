import type { Meta, StoryObj } from "@storybook/svelte";

import Members from "$lib/figma/navigation/side-nav/Members.svelte";

const meta: Meta<Members> = {
    component: Members,
};
export default meta;

type Story = StoryObj<Members>;

export const Default: Story = {};
