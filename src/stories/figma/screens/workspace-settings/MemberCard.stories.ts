import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceUser } from "$lib/storybook";

import MemberCard from "$lib/figma/screens/workspace-settings/MemberCard.svelte";

const meta: Meta<MemberCard> = {
    component: MemberCard,
    args: { workspaceUser },
};
export default meta;

type Story = StoryObj<MemberCard>;

export const Default: Story = {};
