// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { makeStorybookSelect } from "$lib-stories/storybook";

export const activeSetting = makeStorybookSelect({
    "Index": "index",
    "Labels": "labels",
    "Team members": "team-members",
    "Billing": "billing",
});
