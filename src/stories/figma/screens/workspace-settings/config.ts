import { makeStorybookSelect } from "$lib/storybook";

export const activeSetting = makeStorybookSelect({
    "Index": "index",
    "Labels": "labels",
    "Team members": "team-members",
    "Billing": "billing",
});
