import { writable, readable } from "svelte/store";
import type { Meta, StoryObj } from "@storybook/svelte";

import Members from "$lib/figma/navigation/side-nav/Members.svelte";

import { workspaceUserSearchModule } from "$lib/storybook";

import type { WorkspaceUserSearchModule } from "$lib/types/stores";

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
