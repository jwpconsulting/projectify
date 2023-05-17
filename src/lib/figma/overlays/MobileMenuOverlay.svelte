<script lang="ts">
    import { _ } from "svelte-i18n";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import MobileMenu from "$lib/figma/overlays/MobileMenu.svelte";
</script>

<div class="px-2 py-4">
    <MobileMenu />
    <div class="px-4">
        <a href="/dashboard">
            <Button
                style={{ kind: "primary" }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.continue-to-dashboard")}
            />
        </a>
    </div>
</div>
