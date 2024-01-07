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
import type { Meta, StoryObj } from "@storybook/svelte";

import ArchivedWorkspaceBoard from "$lib/figma/cards/ArchivedWorkspaceBoard.svelte";
import { workspaceBoard, mobileParameters } from "$lib/storybook";

const meta: Meta<ArchivedWorkspaceBoard> = {
    component: ArchivedWorkspaceBoard,
    args: {
        workspaceBoard,
    },
};
export default meta;

type Story = StoryObj<ArchivedWorkspaceBoard>;

export const Default: Story = {};

export const Mobile: Story = { parameters: mobileParameters };
