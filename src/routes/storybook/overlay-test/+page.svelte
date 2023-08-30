<script lang="ts">
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";

    const target = {
        kind: "deleteLabel" as const,
        label: { name: "This is a label", color: 0, uuid: "" },
    };

    async function open() {
        await openDestructiveOverlay(target);
    }
</script>

<Button
    action={{ kind: "button", action: open }}
    style={{ kind: "primary" }}
    color="blue"
    size="medium"
    label="Open overlay"
/>
