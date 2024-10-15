// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import FilterLabel from "$lib/figma/select-controls/FilterLabel.svelte";
import type { SelectLabel } from "$lib/figma/types";
import {
    selectLabels,
    makeStorybookSelect,
    mobileParameters,
} from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

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
        checked: { control: "boolean" },
        onEdit: makeStorybookSelect({
            undefined: undefined,
            callback: () => undefined,
        }),
    },
    args: {
        label: "red",
        checked: false,
        onEdit: "undefined",
    },
};
export default meta;

type Story = StoryObj<FilterLabel>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
