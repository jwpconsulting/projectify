<script lang="ts">
    import { onMount } from "svelte";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { keepFocusInside } from "$lib/utils/focus";

    let buttonGroup: HTMLElement;

    let message = "Nothing yet";

    let unfocus: (() => void) | undefined = undefined;

    function action(t: string) {
        message = t;
    }

    function activateFocusLock() {
        if (unfocus) {
            action("Already enabled");
            return;
        }
        unfocus = keepFocusInside(buttonGroup);
        action("Focus lock enabled");
    }

    function deactivateFocusLock() {
        if (!unfocus) {
            action("Already unfocused");
            return;
        }
        unfocus();
    }

    onMount(() => {
        return () => {
            if (unfocus) {
                unfocus();
            }
        };
    });
</script>

<div>
    <p>Status: {message}</p>
    <h1>Commands</h1>
    <Button
        action={{ kind: "button", action: activateFocusLock }}
        style={{ kind: "primary" }}
        size="medium"
        label="Activate focus lock"
        color="blue"
    />
</div>

<div>
    <h1>Unreachable button here:</h1>
    <Button
        action={{ kind: "button", action: () => action("0 was clicked") }}
        style={{ kind: "primary" }}
        size="medium"
        label="0"
        color="red"
    />
</div>

<div
    bind:this={buttonGroup}
    class="rounded-full border-2 border-black p-4 px-32 py-4"
    aria-labelledby="dialog-title"
    aria-describedby="dialog-description"
    role="dialog"
    aria-modal="true"
>
    <h1 id="dialog-title">These can be focused</h1>
    <p id="dialog-description">
        A focus trap should prevent focus from leaving this modal
    </p>
    <Button
        action={{ kind: "button", action: () => action("1 was clicked") }}
        style={{ kind: "primary" }}
        size="medium"
        label="1"
        color="blue"
    />
    <Button
        action={{ kind: "button", action: () => action("2 was clicked") }}
        style={{ kind: "primary" }}
        size="medium"
        label="2"
        color="blue"
    />
    <Button
        action={{ kind: "button", action: deactivateFocusLock }}
        style={{ kind: "primary" }}
        size="medium"
        label="Deactivate focus lock"
        color="blue"
    />
</div>

<div>
    <h1>Unreachable button here:</h1>
    <Button
        action={{ kind: "button", action: () => action("4 was clicked") }}
        style={{ kind: "primary" }}
        size="medium"
        label="4"
        color="red"
    />
</div>
