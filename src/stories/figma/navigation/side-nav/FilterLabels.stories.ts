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

import FilterLabels from "$lib/figma/navigation/side-nav/FilterLabels.svelte";
import type { FilterLabelMenuState } from "$lib/figma/types";
import { makeStorybookSelect, mappedLabels } from "$lib/storybook";

const states = makeStorybookSelect<FilterLabelMenuState>({
    List: { kind: "list" },
    Create: { kind: "create" },
    Update: { kind: "update", label: mappedLabels[0] },
});

const meta: Meta<FilterLabels> = {
    component: FilterLabels,
    argTypes: {
        state: states,
    },
};
export default meta;

type Story = StoryObj<FilterLabels>;

export const List: Story = {
    args: {
        state: "list",
    },
};
export const Create: Story = {
    args: {
        state: "create",
    },
};
export const Update: Story = {
    args: {
        state: "update",
    },
};
