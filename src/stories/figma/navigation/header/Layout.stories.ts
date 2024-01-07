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

import Layout from "$lib/figma/navigation/header/Layout.svelte";
import { mobileParameters } from "$lib/storybook";

const meta: Meta<Layout> = {
    component: Layout,
    argTypes: {},
    args: {
        logoVisibleDesktop: true,
        logoVisibleMobile: true,
    },
};
export default meta;

type Story = StoryObj<Layout>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
