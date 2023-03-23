import { readable } from "svelte/store";
import type { Meta, StoryObj } from "@storybook/svelte";

import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";

import { workspaceBoardSearchModule } from "$lib/storybook";

const meta: Meta<Boards> = {
    component: Boards,
    argTypes: {},
    args: {
        workspaceBoardSearchModule,
    },
};
export default meta;

type Story = StoryObj<Boards>;

export const Default: Story = {};
