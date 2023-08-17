import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace } from "$lib/storybook";

import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";

const meta: Meta<Boards> = {
    component: Boards,
    args: {
        workspace,
    },
};
export default meta;

type Story = StoryObj<Boards>;

export const Default: Story = {};
