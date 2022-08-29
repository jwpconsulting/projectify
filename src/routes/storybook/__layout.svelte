<script lang="ts">
    const links = [
        {
            title: "Navigation",
            href: "/storybook/navigation",
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
            title: "Composites",
            href: "/storybook/composites",
        },
    ];
</script>

<div class="sticky top-0 flex flex-row justify-center gap-4">
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
