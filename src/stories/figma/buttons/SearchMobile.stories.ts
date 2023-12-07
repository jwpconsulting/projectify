import type { Meta, StoryObj } from "@storybook/svelte";

import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";

const meta: Meta<SearchMobile> = {
    component: SearchMobile,
};
export default meta;

type Story = StoryObj<SearchMobile>;

export const Default: Story = {};
