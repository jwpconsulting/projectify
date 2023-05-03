<script lang="ts">
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import Button from "$lib/figma/buttons/Button.svelte";

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
                console.log("Async action performed");
            },
        });
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
<Button
    on:click={openAsync}
    style={{ kind: "primary" }}
    color="blue"
    disabled={false}
    size="medium"
>
    Open async overlay
</Button>
