<script lang="ts">
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";

    const target = {
        kind: "deleteLabel" as const,
        label: { name: "This is a label", color: 0, uuid: "" },
    };

    function open() {
        openDestructiveOverlay(target, {
            kind: "sync",
            action: () => {
                console.log("Action performed");
            },
        });
    }

    function openAsync() {
        openDestructiveOverlay(target, {
            kind: "async",
            action: async () => {
                await new Promise((resolve) => resolve(null));
                console.log("Async action performed");
            },
        });
    }
</script>

<Button
    action={{ kind: "button", action: open }}
    style={{ kind: "primary" }}
    color="blue"
    disabled={false}
    size="medium"
    label="Open overlay"
/>
<Button
    action={{ kind: "button", action: openAsync }}
    style={{ kind: "primary" }}
    color="blue"
    disabled={false}
    size="medium"
    label="Open async overlay"
/>
