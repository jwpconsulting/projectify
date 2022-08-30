<script lang="ts">
    import DestructiveOverlayContainer from "$lib/components/DestructiveOverlayContainer.svelte";
    import { destructiveOverlayState } from "$lib/stores/global-ui";
    import Button from "$lib/figma/Button.svelte";
    const target = {
        kind: "deleteLabel" as const,
        label: { name: "This is a label", color: 0, uuid: "" },
    };

    function open() {
        $destructiveOverlayState = {
            kind: "visible",
            target,
        };
    }
</script>

<Button
    on:click={open}
    style={{ kind: "primary" }}
    color="blue"
    disabled={false}
    size="medium"
>
    Open overlay
</Button>
<DestructiveOverlayContainer fixed={false} />
