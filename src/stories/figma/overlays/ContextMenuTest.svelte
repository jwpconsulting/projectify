<script lang="ts">
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";

    export let type: ContextMenuType;

    let status = "Nothing happened yet";

    async function open(target: HTMLElement) {
        status = "Opening context menu";
        const promise = openContextMenu(type, target);
        status = "The context menu is open";
        await promise;
        status = "The context menu is closed";
    }

    let button1: HTMLElement;
    let button2: HTMLElement;
    let button3: HTMLElement;
    let button4: HTMLElement;
    let button5: HTMLElement;
</script>

<div class="flex h-screen flex-col justify-between">
    <div class="flex flex-row justify-between">
        <div bind:this={button1}>
            <Button
                action={{ kind: "button", action: () => open(button1) }}
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                label="Left"
            />
        </div>
        <div bind:this={button2}>
            <Button
                action={{ kind: "button", action: () => open(button2) }}
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                label="Right"
            />
        </div>
    </div>
    <div class="flex flex-row justify-center">
        <div class="flex flex-col items-center gap-4">
            <p>
                Current status: {status}
            </p>
            <div bind:this={button3}>
                <Button
                    action={{ kind: "button", action: () => open(button3) }}
                    style={{ kind: "primary" }}
                    color="blue"
                    size="medium"
                    label="Center"
                />
            </div>
        </div>
    </div>
    <div class="flex flex-row justify-between">
        <div bind:this={button4}>
            <Button
                action={{ kind: "button", action: () => open(button4) }}
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                label="Left"
            />
        </div>
        <div bind:this={button5}>
            <Button
                action={{ kind: "button", action: () => open(button5) }}
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                label="Right"
            />
        </div>
    </div>
</div>

<ContextMenuContainer />
