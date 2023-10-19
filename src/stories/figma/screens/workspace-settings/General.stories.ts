import type { Meta, StoryObj } from "@storybook/svelte";

import General from "$lib/figma/screens/workspace-settings/General.svelte";
import { workspace } from "$lib/storybook";

const meta: Meta<General> = {
    component: General,
    args: { workspace },
};
export default meta;

type Story = StoryObj<General>;

export const Default: Story = {};
