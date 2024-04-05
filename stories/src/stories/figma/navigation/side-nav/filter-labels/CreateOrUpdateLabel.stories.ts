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

import CreateOrUpdateLabel from "$lib/figma/navigation/side-nav/filter-labels/CreateOrUpdateLabel.svelte";
import { makeStorybookSelect, mappedLabels } from "$lib/storybook";

const states = makeStorybookSelect({
    "Create label": { kind: "create" },
    "Update label": { kind: "update", label: mappedLabels[0] },
});

const meta: Meta<CreateOrUpdateLabel> = {
    component: CreateOrUpdateLabel,
    argTypes: { state: states },
};
export default meta;

type Story = StoryObj<CreateOrUpdateLabel>;

export const Create: Story = {
    args: { state: "create-label" },
};

export const Update: Story = {
    args: { state: "update-label" },
};
