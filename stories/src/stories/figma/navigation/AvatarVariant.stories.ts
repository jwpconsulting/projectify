// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
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

import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
import { makeStorybookSelect, user1, user2 } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";
import type { AvatarStateSize } from "$lib/figma/types";

const meta: Meta<AvatarVariant> = {
    component: AvatarVariant,
    argTypes: {
        size: makeStorybookSelect<AvatarStateSize>({
            Medium: "medium",
            Large: "large",
        }),
    },
};
export default meta;

type Story = StoryObj<AvatarVariant>;

export const Default: Story = {
    args: {
        size: "medium",
        content: {
            kind: "single",
            user: null,
        },
    },
};

export const User1: Story = {
    args: {
        size: "medium",
        content: {
            kind: "single",
            user: user1,
        },
    },
};

export const User2: Story = {
    args: {
        size: "medium",
        content: {
            kind: "single",
            user: user2,
        },
    },
};

export const Multiple: Story = {
    args: {
        size: "medium",
        content: {
            kind: "multiple",
            users: [user1, user2],
        },
    },
};

export const Assign: Story = {
    args: {
        size: "medium",
        content: {
            kind: "assign",
            users: [user1, user2],
        },
    },
};
