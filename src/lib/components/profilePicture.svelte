<script lang="ts">
    import IconUserProfile from "./icons/icon-user-profile.svelte";
    import vars from "$lib/env";
    import IconPlus from "./icons/icon-plus.svelte";
    import IconClose from "./icons/icon-close.svelte";
    import IconUserPlusFill from "./icons/icon-user-plus-fill.svelte";

    export let size = 32;
    export let url: string = null;
    export let prefix = vars.API_ENDPOINT;
    export let showPlus = false;
    export let emptyIcon = IconUserProfile;
    export let typogram: string = null;

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
        class="flex shrink-0 items-center justify-center rounded-3xl border border-dashed border-primary text-primary hover:ring"
    >
        <IconUserPlusFill />
    </div>
{:else}
    <div
        style={`width: ${sizePx}; height: ${sizePx};`}
        class="flex justify-center items-center shrink-0"
    >
        {#if src}
            {#if loadingError}
                <IconClose />
            {:else}
                <img
                    class="object-cover pointer-events-none"
                    draggable="false"
                    width="100%"
                    height="100%"
                    {src}
                    alt="user"
                    on:error={() => (loadingError = true)}
                />
            {/if}
        {:else if emptyIcon}
            <svelte:component this={emptyIcon} />
        {:else if typogram}
            <svg viewBox="-50 -50 100 100" preserveAspectRatio="xMidYMid meet">
                <text
                    x="0px"
                    y="0px"
                    font-size="30"
                    dy=".35em"
                    text-anchor="middle"
                    class="uppercase font-bold"
                    fill="currentColor"
                    >{typogram.substring(0, 2)}
                </text>
            </svg>
        {/if}
    </div>
{/if}
