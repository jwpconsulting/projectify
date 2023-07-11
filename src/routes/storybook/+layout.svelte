<script lang="ts">
    const links = [
        {
            title: "Typography",
            href: "/storybook/typography",
        },
        {
            title: "Buttons",
            href: "/storybook/buttons",
        },
        {
            title: "Select controls",
            href: "/storybook/select-controls",
        },
        {
            title: "Dropdown",
            href: "/storybook/dropdown",
        },
        {
            title: "Navigation",
            href: "/storybook/navigation",
        },
        {
            title: "Screens",
            href: "/storybook/screens",
        },
        {
            title: "Overlays",
            href: "/storybook/overlays",
        },
        {
            title: "Overlay test",
            href: "/storybook/overlay-test",
        },
        {
            title: "Context menu test",
            href: "/storybook/context-menu-test",
        },
    ];
</script>

<div class="sticky top-0 flex flex-row flex-wrap justify-center gap-4">
    {#each links as link}
        <a
            href={link.href}
            class="rounded-llg border border-2 bg-base-100 px-4 py-2 font-bold"
            >{link.title}</a
        >
    {/each}
</div>
<div class="flex flex-col">
    <slot />
</div>
