<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeaderButton from "$lib/funabashi/buttons/HeaderButton.svelte";
    import { closeMobileMenu } from "$lib/stores/globalUi";

    $: links = [
        { label: $_("header.features"), href: "/features" },
        { label: $_("header.solutions"), href: "/solutions" },
        { label: $_("header.help"), href: "/help" },
        { label: $_("header.pricing"), href: "/pricing" },
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
