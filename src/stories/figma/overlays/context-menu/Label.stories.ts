import type { Meta, StoryObj } from "@storybook/svelte";

import Label from "$lib/figma/overlays/context-menu/Label.svelte";
import { labelAssignment } from "$lib/storybook";

const meta: Meta<Label> = {
    component: Label,
    args: { labelAssignment },
};
export default meta;

type Story = StoryObj<Label>;

export const Default: Story = {};
