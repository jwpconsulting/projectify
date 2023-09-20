import type { Meta, StoryObj } from "@storybook/svelte";

import Permissions from "$lib/figma/overlays/context-menu/Permissions.svelte";

const meta: Meta<Permissions> = {
    component: Permissions,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Permissions>;

export const Default: Story = {};
