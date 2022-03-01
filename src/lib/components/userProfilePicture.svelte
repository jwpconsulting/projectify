<script lang="ts">
    import IconUserProfile from "./icons/icon-user-profile.svelte";
    import vars from "$lib/env";
    import IconPlus from "./icons/icon-plus.svelte";
    import IconClose from "./icons/icon-close.svelte";
    export let size = 32;
    export let url: string = null;
    export let prefix = vars.API_ENDPOINT;
    export let showPlus = false;

    let src: string = null;

    let loadingError = false;

    $: {
        if (url) {
            let usePrefix =
                url.indexOf("data:") !== 0 && url.indexOf("http") !== 0;
            src = usePrefix ? prefix + url : url;
            loadingError = false;
        } else {
            src = null;
        }
    }
    $: sizePx = size + "px";
</script>

{#if !url && showPlus}
    <div
        style={`width: ${sizePx}; height: ${sizePx};`}
        class="flex justify-center items-center overflow-hidden rounded-full shrink-0 border-2 border-primary text-primary border-dotted hover:ring"
    >
        <IconPlus />
    </div>
{:else}
    <div
        class:ring-2={size <= 32}
        class:ring-4={size > 32}
        style={`width: ${sizePx}; height: ${sizePx};`}
        class="flex justify-center items-center overflow-hidden rounded-full shrink-0 bg-secondary text-base-100"
    >
        {#if src}
            {#if loadingError}
                <IconClose />
            {:else}
                <img
                    class="object-cover"
                    draggable="false"
                    width="100%"
                    height="100%"
                    {src}
                    alt="user"
                    on:error={() => (loadingError = true)}
                />
            {/if}
        {:else}
            <IconUserProfile />
        {/if}
    </div>
{/if}
