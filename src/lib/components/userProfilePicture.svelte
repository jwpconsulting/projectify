<script lang="ts">
    import IconUserProfile from "./icons/icon-user-profile.svelte";
    import vars from "$lib/env";
    export let size = 32;
    export let url: string = null;
    export let prefix = vars.API_ENDPOINT;

    let src: string = null;

    $: {
        if (url) {
            let usePrefix =
                url.indexOf("data:") !== 0 && url.indexOf("http") !== 0;
            src = usePrefix ? prefix + url : url;
        } else {
            src = null;
        }
    }
    $: sizePx = size + "px";
</script>

<div
    class:ring-2={size <= 32}
    class:ring-4={size > 32}
    style={`width: ${sizePx}; height: ${sizePx};`}
    class="m-1 flex overflow-hidden rounded-full shrink-0 bg-secondary text-base-100"
>
    {#if src}
        <img
            class="object-cover"
            draggable="false"
            width="100%"
            height="100%"
            {src}
            alt="user"
        />
    {:else}
        <IconUserProfile />
    {/if}
</div>
