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
import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const state = {
    kind: "new-workspace",
    title: "Hello world",
};

const meta: Meta<DashboardPlaceholder> = {
    component: DashboardPlaceholder,
    args: { state },
};
export default meta;

type Story = StoryObj<DashboardPlaceholder>;

export const Default: Story = {};
