import type { Meta, StoryObj } from "@storybook/svelte";

import { task, workspaceBoardSection } from "$lib/storybook";

import MenuButton from "$lib/figma/cards/task-card/MenuButton.svelte";

const meta: Meta<MenuButton> = {
    component: MenuButton,
    args: {
        task,
        workspaceBoardSection,
    },
};
export default meta;

type Story = StoryObj<MenuButton>;

export const Default: Story = {};
