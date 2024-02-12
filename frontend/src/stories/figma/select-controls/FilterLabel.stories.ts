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

import FilterLabel from "$lib/figma/select-controls/FilterLabel.svelte";
import type { SelectLabel } from "$lib/figma/types";
import {
    selectLabels,
    makeStorybookSelect,
    mobileParameters,
} from "$lib/storybook";

const short: SelectLabel = {
    label: {
        uuid: "does-not-exist",
        name: "short label",
        color: 0,
    },
    kind: "label",
};

const labelTuples: [string, SelectLabel][] = selectLabels.map((l) =>
    l.kind === "label"
        ? [
              l.label.name,
              {
                  ...l,
                  label: {
                      ...l.label,
                      name: "Long long long name, I made sure of that. It is very long. Watch how long it is. This is how we test the limits of our knowledge of phsyics. This might as well usher in the beginning of a unifying theory of matter. Watch my TedX talk.",
                  },
              },
          ]
        : [l.kind, l],
);
const label: Record<string, SelectLabel> = {
    ...Object.fromEntries(labelTuples),
    short: short,
};

const meta: Meta<FilterLabel> = {
    component: FilterLabel,
    argTypes: {
        label: makeStorybookSelect(label),
    },
    args: {
        label: "red",
        checked: false,
        canEdit: false,
    },
};
export default meta;

type Story = StoryObj<FilterLabel>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
