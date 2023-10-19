import { makeStorybookSelect } from "$lib/storybook";

export const activeSetting = makeStorybookSelect({
    "Index": "index",
    "Labels": "labels",
    "Workspace users": "workspace-users",
    "Billing": "billing",
});
