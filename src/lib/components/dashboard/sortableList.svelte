<script lang="ts">
    import { draggable } from "$lib/actions/draggable";
    import { quintOut } from "svelte/easing";
    import { crossfade } from "svelte/transition";
    import { flip } from "svelte/animate";

    export let list;
    export let key;
    export let isDragging = false;
    export let containerCSS = "";

    const [send, receive] = crossfade({
        fallback(node, params) {
            const style = getComputedStyle(node);
            const transform =
                style.transform === "none" ? "" : style.transform;

            return {
                duration: 100,
                easing: quintOut,
                css: (t) => `
        transform: ${transform} scale(${t});
        opacity: ${t}
      `,
            };
        },
    });
</script>

<div class={containerCSS}>
    {#each list as item, inx (item[key])}
        <!-- 
            in:send={{ key: item[key] }}
            out:send={{ key: item[key] }} 
        -->
        <div
            use:draggable={{ moveToBody: true }}
            on:dragStart={() => (isDragging = true)}
            on:dragEnd={() => (isDragging = false)}
        >
            <slot {item} {inx} />
        </div>
    {/each}
    {#if !isDragging}
        <slot name="footer" />
    {/if}
</div>
