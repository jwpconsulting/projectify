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

import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";

const meta: Meta<Checkbox> = {
    component: Checkbox,
    argTypes: {
        contained: {
            control: "boolean",
        },
        checked: {
            control: "boolean",
        },
        disabled: {
            control: "boolean",
        },
    },
    args: {
        checked: false,
        contained: false,
        disabled: false,
    },
};
export default meta;

type Story = StoryObj<Checkbox>;

export const Default: Story = {};

export const DisabledChecked: Story = {
    args: { checked: true, disabled: true },
};

export const DisabledUnchecked: Story = {
    args: { checked: false, disabled: true },
};
