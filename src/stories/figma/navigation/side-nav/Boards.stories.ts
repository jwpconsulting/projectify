import type { Meta, StoryObj } from "@storybook/svelte";

import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";
import { workspace } from "$lib/storybook";

const meta: Meta<Boards> = {
    component: Boards,
    args: {
        workspace,
    },
};
export default meta;

type Story = StoryObj<Boards>;

export const Default: Story = {};
