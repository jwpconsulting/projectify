<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeaderButton from "$lib/funabashi/buttons/HeaderButton.svelte";
    import { closeMobileMenu } from "$lib/stores/globalUi";

    $: links = [
        { label: $_("navigation.header.features"), href: "/features" },
        { label: $_("navigation.header.solutions"), href: "/solutions" },
        { label: $_("navigation.header.help"), href: "/help" },
        { label: $_("navigation.header.pricing"), href: "/pricing" },
    ];
</script>

<div class="flex flex-col gap-4 divide-y divide-border">
    {#each links as link}
        <div>
            <HeaderButton
                action={{
                    kind: "a",
                    href: link.href,
                    onInteract: closeMobileMenu,
                }}
                type={{ kind: "button" }}
                label={link.label}
            />
        </div>
    {/each}
</div>
