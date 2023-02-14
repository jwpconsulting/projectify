import HeaderButton from "$lib/figma/buttons/HeaderButton.svelte";

export default {
    component: HeaderButton,
};

export const Dropdown = () => ({
    Component: HeaderButton,
    props: {
        label: "Button",
        open: true,
        type: "dropdown",
    },
});

export const Button = () => ({
    Component: HeaderButton,
    props: {
        label: "Button",
        open: true,
        type: "button",
    },
});
