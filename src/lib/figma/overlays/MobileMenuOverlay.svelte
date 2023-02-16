<script lang="ts">
    import { _ } from "svelte-i18n";
    import Button from "$lib/figma/buttons/Button.svelte";
    import MobileMenu from "$lib/figma/overlays/MobileMenu.svelte";
</script>

<div class="py-4 px-2">
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
