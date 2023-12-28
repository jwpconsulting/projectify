import type { Meta, StoryObj } from "@storybook/svelte";

import { makeStorybookSelect } from "$lib/storybook";
import LogIn from "$routes/(storefront)/(auth)/user/log-in/+page.svelte";

const data = makeStorybookSelect({
    "With redirect": {
        redirectTo: "a/nested/url?yo",
    },
    "Without redirect": {
        redirectTo: undefined,
    },
});

const meta: Meta<LogIn> = {
    component: LogIn,
    argTypes: { data },
};
export default meta;

type Story = StoryObj<LogIn>;

export const Default: Story = {
    args: { data: "with-redirect" },
};

export const WithoutRedirect: Story = {
    args: { data: "without-redirect" },
};
