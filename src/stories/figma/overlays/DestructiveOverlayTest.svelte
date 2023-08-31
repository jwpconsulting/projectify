<script lang="ts">
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        destructiveOverlayState,
        openDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { DestructiveOverlayType } from "$lib/types/ui";

    export let target: DestructiveOverlayType;

    let disabled = false;
    let result = "";

    async function openDestructive() {
        disabled = true;
        result = "waiting";
        try {
            await openDestructiveOverlay(target);
            result = "resolved";
        } catch {
            result = "rejected";
        } finally {
            disabled = false;
        }
    }
</script>

<p>
    Result: {result}
</p>
<Button
    action={{ kind: "button", action: openDestructive, disabled }}
    style={{ kind: "primary" }}
    color="red"
    size="medium"
    label="Open destructive overlay"
/>

<OverlayContainer store={destructiveOverlayState} let:target>
    <DestructiveOverlay {target} />
</OverlayContainer>
