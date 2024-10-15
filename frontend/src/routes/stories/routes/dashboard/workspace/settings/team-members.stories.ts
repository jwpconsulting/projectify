// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import { workspace, makeStorybookSelect, user1 } from "$lib-stories/storybook";
import type { User } from "$lib/types/user";
import type { WorkspaceDetail } from "$lib/types/workspace";
import TeamMembers from "$routes/(platform)/dashboard/workspace/[workspaceUuid]/settings/team-members/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

// XXX duplicated because we can't import ./$types
interface PageData {
    user: User;
    workspace: WorkspaceDetail;
}

const data = makeStorybookSelect<PageData>({
    "Regular workspace": {
        user: user1,
        workspace,
    },
});

const meta: Meta<TeamMembers> = {
    component: TeamMembers,
    argTypes: { data },
    args: { data: "regular-workspace" },
};
export default meta;

type Story = StoryObj<TeamMembers>;

export const RegularWorkspace: Story = { args: { data: "regular-workspace" } };
