<script lang="ts">
    import { draggable } from "$lib/actions/draggable";
    import { quintOut } from "svelte/easing";
    import { crossfade } from "svelte/transition";
    import { flip } from "svelte/animate";
    import { arrayMoveImmutable } from "array-move";

    export let list;
    export let key;
    export let isDragging = false;
    export let containerCSS = "";

    let dragingItem = null;
    let dragingIndex = -1;
    let startDragingIndex = -1;
    let dragoverItem = null;
    let dragoverIndex = -1;

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

    let startList;

    function onDragStart(event, item, inx) {
        isDragging = true;

        dragingItem = item;
        dragingIndex = inx;
        startDragingIndex = inx;

        startList = [...list];
    }
    function onDragEnd(event, item, inx) {
        isDragging = false;

        console.log(
            "Drop move from",
            startDragingIndex,
            " to ",
            dragoverIndex
        );
        list = arrayMoveImmutable(startList, startDragingIndex, dragoverIndex);

        dragingItem = null;
        dragingIndex = -1;

        dragoverItem = null;
        dragoverIndex = -1;
    }

    function onDragOverItem(event, item, inx) {
        dragoverItem = item;
        dragoverIndex = inx;

        const fromInx = dragingIndex;
        const toInx = inx;

        if (fromInx == toInx) {
            return;
        }

        list = arrayMoveImmutable(list, fromInx, toInx);
        dragingIndex = inx;
    }

    const flipOpts = {
        duration(d) {
            return d;
        },
    };
</script>

<div class={containerCSS}>
    {#each list as item, inx (item[key])}
        <div
            in:send={{ key: item[key] }}
            out:send={{ key: item[key] }}
            animate:flip={flipOpts}
            class="sortable-item"
            use:draggable={{ moveToBody: true }}
            on:dragstart={(e) => onDragStart(e, item, inx)}
            on:dragend={(e) => onDragEnd(e, item, inx)}
            on:dragover={(e) => onDragOverItem(e, item, inx)}
        >
            <slot {item} {inx} />
        </div>
    {/each}
    {#if !isDragging}
        <slot name="footer" />
    {/if}
</div>
