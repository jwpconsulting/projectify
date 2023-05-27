import type { Meta, StoryObj } from "@storybook/svelte";

import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";

const meta: Meta<Boards> = {
    component: Boards,
    argTypes: {},
    args: {},
};
export default meta;

type Story = StoryObj<Boards>;

export const Default: Story = {};
