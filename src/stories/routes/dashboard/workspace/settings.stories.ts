// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2024 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace, makeStorybookSelect, user1 } from "$lib/storybook";
import type { User } from "$lib/types/user";
import type { Workspace } from "$lib/types/workspace";
import Settings from "$routes/(platform)/dashboard/workspace/[workspaceUuid]/settings/+page.svelte";

// XXX duplicated because we can't import ./$types
interface PageData {
    user: User;
    workspace: Workspace;
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
