<script lang="ts">
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";
    import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        constructiveOverlayState,
        destructiveOverlayState,
        openConstructiveOverlay,
        openDestructiveOverlay,
    } from "$lib/stores/globalUi";

    let disabled = false;
    let result = "";

    async function openDestructive() {
        disabled = true;
        result = "waiting";
        try {
            await openDestructiveOverlay({
                kind: "deleteLabel" as const,
                label: { name: "This is a label", color: 0, uuid: "" },
            });
            result = "resolved";
        } catch {
            result = "rejected";
        } finally {
            disabled = false;
        }
    }

    async function openConstructive() {
        disabled = true;
        result = "waiting";
        try {
            await openConstructiveOverlay({ kind: "skipOnboarding" });
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
<Button
    action={{ kind: "button", action: openConstructive, disabled }}
    style={{ kind: "primary" }}
    color="blue"
    size="medium"
    label="Open constructive overlay"
/>

<OverlayContainer store={destructiveOverlayState} let:target>
    <DestructiveOverlay {target} />
</OverlayContainer>

<OverlayContainer store={constructiveOverlayState} let:target>
    <ConstructiveOverlay {target} />
</OverlayContainer>
