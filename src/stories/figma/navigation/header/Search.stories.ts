import type { Meta, StoryObj } from "@storybook/svelte";

import { mobileParameters } from "$lib/storybook";

import Search from "$lib/figma/navigation/header/Search.svelte";

const meta: Meta<Search> = {
    component: Search,
    argTypes: {},
    args: {},
};
export default meta;

type Story = StoryObj<Search>;

export const Desktop: Story = {};
export const Mobile: Story = {
    parameters: mobileParameters,
};
