<script lang="ts">
    import IconUserProfile from "./icons/icon-user-profile.svelte";
    import { createEventDispatcher } from "svelte";

    import IconPhotocamera from "./icons/icon-photocamera.svelte";

    import ProfilePicture from "./profilePicture.svelte";

    export let url = null;
    let inputFileRef = null;

    const dispatch = createEventDispatcher();

    $: src = url ? url : null;

    function onSelectFileClick() {
        inputFileRef.click();
    }
    function onFileSelected(event) {
        const file = event.target.files[0];
        if (!file) {
            return;
        }

        const reader = new FileReader();
        reader.addEventListener("load", (event) => {
            src = event.target.result as string;
            dispatch("fileSelected", { src, file });
        });
        reader.readAsDataURL(file);
    }
</script>

<div class="relative">
    {#if $$slots.default}
        <slot {src} />
    {:else}
        <ProfilePicture size={128} url={src} />
    {/if}
    <input
        bind:this={inputFileRef}
        type="file"
        class="hidden"
        accept=".jpg, .jpeg, .png"
        on:change={onFileSelected}
    />
    <button
        on:click={onSelectFileClick}
        class="children-first:w-2 btn btn-circle btn-primary absolute bottom-[-8px] right-[-8px] bg-primary-content text-primary shadow-lg hover:bg-secondary"
        ><IconPhotocamera /></button
    >
</div>
