<script lang="ts">
    import Button from "$lib/figma/buttons/Button.svelte";
    import { openContextMenu } from "$lib/stores/globalUi";

    function open(target: HTMLElement) {
        openContextMenu({ kind: "profile" }, target);
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
                on:click={() => open(button1)}
                style={{ kind: "primary" }}
                color="blue"
                disabled={false}
                size="medium"
                label="Left"
            />
        </div>
        <div bind:this={button2}>
            <Button
                on:click={() => open(button2)}
                style={{ kind: "primary" }}
                color="blue"
                disabled={false}
                size="medium"
                label="Right"
            />
        </div>
    </div>
    <div class="flex flex-row justify-center">
        <div bind:this={button3}>
            <Button
                on:click={() => open(button3)}
                style={{ kind: "primary" }}
                color="blue"
                disabled={false}
                size="medium"
                label="Center"
            />
        </div>
    </div>
    <div class="flex flex-row justify-between">
        <div bind:this={button4}>
            <Button
                on:click={() => open(button4)}
                style={{ kind: "primary" }}
                color="blue"
                disabled={false}
                size="medium"
                label="Left"
            />
        </div>
        <div bind:this={button5}>
            <Button
                on:click={() => open(button5)}
                style={{ kind: "primary" }}
                color="blue"
                disabled={false}
                size="medium"
                label="Right"
            />
        </div>
    </div>
</div>
