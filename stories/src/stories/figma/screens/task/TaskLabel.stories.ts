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

import TaskLabel from "$lib/figma/screens/task/TaskLabel.svelte";
import { makeStorybookSelect, mappedLabels } from "$lib/storybook";
import type { Label } from "$lib/types/workspace";

const meta: Meta<TaskLabel> = {
    component: TaskLabel,
    argTypes: {
        labels: makeStorybookSelect<Label[]>({
            "0 labels selected": [],
            "1 labels selected": mappedLabels.slice(0, 1),
            "3 labels selected": mappedLabels.slice(1, 4),
        }),
    },
    args: {
        labels: "3-labels-selected",
    },
};
export default meta;

type Story = StoryObj<TaskLabel>;

export const Default: Story = {};

export const ApplyLabel: Story = {
    args: {
        labels: "0-labels-selected",
    },
};
