import type { Meta, StoryObj } from "@storybook/svelte";

import UserDropdownClosedNav from "$lib/figma/buttons/UserDropdownClosedNav.svelte";
import { workspaceUserSearchModule } from "$lib/storybook";

const meta: Meta<UserDropdownClosedNav> = {
    component: UserDropdownClosedNav,
    argTypes: {},
    args: {
        workspaceUserSearchModule,
    },
};
export default meta;

type Story = StoryObj<UserDropdownClosedNav>;

export const Default: Story = {};
