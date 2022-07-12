<script lang="ts">
    import { draggable } from "$lib/actions/draggable";
    import { quintOut } from "svelte/easing";
    import { crossfade } from "svelte/transition";
    import { flip } from "svelte/animate";
    import { arrayMoveImmutable } from "array-move";
    import debounce from "lodash/debounce";
    import { createEventDispatcher } from "svelte";

    export let list: any[];
    export let listUUID: string;
    export let key: any;
    export let isDragging = false;
    export let containerCSS = "";

    let dragingIndex: number = -1;
    let startDragingIndex: number = -1;
    let dragoverIndex: number = -1;

    const dispatch = createEventDispatcher();

    crossfade({
        fallback(node: HTMLElement, _params: any) {
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

    let startList: any[];

    function onDragStart(_event: DragEvent, _item: any, inx: number) {
        isDragging = true;

        dragingIndex = inx;
        startDragingIndex = inx;

        startList = [...list];
    }
    function onDragEnd(_event: DragEvent, _item: any, _inx: number) {
        isDragging = false;

        list = arrayMoveImmutable(startList, startDragingIndex, dragoverIndex);
        dispatch("sorting", {
            listUUID,
            fromIndex: startDragingIndex,
            toIndex: dragoverIndex,
        });

        dragingIndex = -1;

        dragoverIndex = -1;
    }

    function onDragOverItem(_event: DragEvent, _item: any, inx: number) {
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
        duration(d: number) {
            return d;
        },
    };
</script>

<div class={containerCSS}>
    {#each list as item, inx (item[key])}
        <div
            animate:flip={flipOpts}
            class="sortable-item"
            use:draggable={{ moveToBody: true }}
            on:dragstart={(e) => onDragStart(e, item, inx)}
            on:dragend={(e) => onDragEnd(e, item, inx)}
            on:dragover={debounce((e) => onDragOverItem(e, item, inx), 100)}
        >
            <slot {item} {inx} />
        </div>
    {/each}
    {#if !isDragging}
        <slot name="footer" />
    {/if}
</div>
