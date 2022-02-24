<script lang="ts">
    import { createEventDispatcher } from "svelte";

    import IconPhotocamera from "./icons/icon-photocamera.svelte";

    import UserProfilePicture from "./userProfilePicture.svelte";

    export let user = null;

    let inputFileRef = null;

    const dispatch = createEventDispatcher();

    $: src = user ? user.profilePicture : null;

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
    <UserProfilePicture size={128} url={src} />
    <input
        bind:this={inputFileRef}
        type="file"
        class="hidden"
        accept=".jpg, .jpeg, .png"
        on:change={onFileSelected}
    />
    <button
        on:click={onSelectFileClick}
        class="absolute bottom-0 right-0 btn shadow-lg btn-circle children-first:w-2 text-primary"
        ><IconPhotocamera /></button
    >
</div>
