<script lang="ts">
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        constructiveOverlayState,
        openConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { ConstructiveOverlayType } from "$lib/types/ui";

    export let target: ConstructiveOverlayType;

    let disabled = false;
    let result = "";

    async function openConstructive() {
        disabled = true;
        result = "waiting";
        try {
            await openConstructiveOverlay(target);
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
    action={{ kind: "button", action: openConstructive, disabled }}
    style={{ kind: "primary" }}
    color="blue"
    size="medium"
    label="Open constructive overlay"
/>

<OverlayContainer store={constructiveOverlayState} let:target>
    <ConstructiveOverlay {target} />
</OverlayContainer>
