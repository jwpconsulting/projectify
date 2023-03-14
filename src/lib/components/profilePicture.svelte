<script lang="ts">
    import IconUserProfile from "$lib/components/icons/icon-user-profile.svelte";
    import vars from "$lib/env";
    import IconClose from "$lib/components/icons/icon-close.svelte";
    import IconUserPlusFill from "$lib/components/icons/icon-user-plus-fill.svelte";

    export let size = 32;
    export let url: string | null = null;
    export let prefix = vars.API_ENDPOINT;
    export let showPlus = false;
    export let emptyIcon: any | null = IconUserProfile;
    export let typogram: string | null = null;

    let src: string | null = null;

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
        class="flex shrink-0 items-center justify-center"
    >
        {#if src}
            {#if loadingError}
                <IconClose />
            {:else}
                <img
                    class="pointer-events-none object-cover"
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
                    class="font-bold uppercase"
                    fill="currentColor"
                    >{typogram.substring(0, 2)}
                </text>
            </svg>
        {/if}
    </div>
{/if}
