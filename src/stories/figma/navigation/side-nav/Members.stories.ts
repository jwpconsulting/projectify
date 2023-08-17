import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceUserSearchModule } from "$lib/storybook";

import Members from "$lib/figma/navigation/side-nav/Members.svelte";

const meta: Meta<Members> = {
    component: Members,
    argTypes: {},
    args: {
        workspaceUserSearchModule,
    },
};
export default meta;

type Story = StoryObj<Members>;

export const Default: Story = {};
