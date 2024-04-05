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
import { mobileParameters } from "$lib/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

import { constructiveOverlays } from "./config";
import ConstructiveOverlayTest from "./ConstructiveOverlayTest.svelte";

const meta: Meta<ConstructiveOverlayTest> = {
    component: ConstructiveOverlayTest,
    argTypes: {
        target: constructiveOverlays,
    },
    args: {
        target: "update-project",
    },
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<ConstructiveOverlayTest>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
