// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK

import { workspace, makeStorybookSelect, user1 } from "$lib-stories/storybook";
import type { User } from "$lib/types/user";
import type { WorkspaceDetail } from "$lib/types/workspace";
import Settings from "$routes/(platform)/dashboard/workspace/[workspaceUuid]/settings/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

// XXX duplicated because we can't import ./$types
interface PageData {
    user: User;
    workspace: WorkspaceDetail;
}

const data = makeStorybookSelect<PageData>({
    Workspace: {
        user: user1,
        workspace,
    },
});

const meta: Meta<Settings> = {
    component: Settings,
    argTypes: { data },
    args: { data: "workspace" },
};
export default meta;

type Story = StoryObj<Settings>;

export const Default: Story = {};
