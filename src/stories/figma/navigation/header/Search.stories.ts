import type { Meta, StoryObj } from "@storybook/svelte";

import Search from "$lib/figma/navigation/header/Search.svelte";
import { mobileParameters } from "$lib/storybook";

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
