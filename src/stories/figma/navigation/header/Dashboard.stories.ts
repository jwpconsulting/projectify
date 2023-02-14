import Dashboard from "$lib/figma/navigation/header/Dashboard.svelte";
import { mobileParameters, user1 } from "$lib/storybook";

const component = Dashboard;
const props = { user: user1 };

export default {
    component,
};

export const Default = () => ({
    Component: component,
    props,
});

export const Mobile = () => ({
    Component: component,
    props,
});
Mobile.parameters = mobileParameters;
