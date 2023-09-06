import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace } from "$lib/storybook";

import Members from "$lib/figma/screens/workspace-settings/Members.svelte";

const meta: Meta<Members> = {
    component: Members,
    args: { workspace },
};
export default meta;

type Story = StoryObj<Members>;

export const Default: Story = {};
