<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { Camera } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    export let label: string;
    export let fileSelected: (file: File) => void;
    let inputFileRef: HTMLElement;

    function click() {
        inputFileRef.click();
    }

    function onFileSelected(event: Event) {
        const eventTarget = event.target;
        if (!(eventTarget instanceof HTMLInputElement)) {
            throw new Error("Expected HTMLInputElement");
        }
        if (!eventTarget.files) {
            throw new Error("Expected eventTarget.files");
        }
        const file = eventTarget.files.item(0);
        if (!file) {
            throw new Error("Expected file");
        }
        fileSelected(file);
    }
</script>

<button
    class="focus:border-focus group h-14 w-14 rounded-full border border-transparent p-0.5"
    on:click={click}
    type="button"
    name="picture"
    aria-label={label}
>
    <input
        bind:this={inputFileRef}
        type="file"
        class="hidden"
        accept=".jpg, .jpeg, .png"
        on:change={onFileSelected}
    />
    <div
        class="rounded-full border border-primary bg-foreground p-3 text-primary group-hover:bg-secondary-hover group-active:bg-disabled"
    >
        <Icon src={Camera} theme="outline" />
    </div>
</button>
