<script lang="ts">
    import IconEdit from "../icons/icon-edit.svelte";
    import IconTrash from "../icons/icon-trash.svelte";
    import IconChevronRight from "../icons/icon-chevron-right.svelte";

    export let section;
    export let index = 0;

    let open = false;

    function toggleOpen() {
        open = !open;
    }

    let contentHeght = 0;
    $: openHeight = open ? contentHeght : 0;
    $: openArrowDeg = open ? 90 : 0;

    function onEdit() {
        console.log("edit");
    }
    function onDelete() {
        console.log("delete");
    }
</script>

<div class="flex m-2 bg-base-100">
    <div
        class="w-1 shrink-0"
        style={`background-color: hsl(${index * 36}, 80%, 60%);`}
    />
    <div class="flex grow flex-col">
        <header
            class="select-none flex items-center h-16 p-2  children:m-1 cursor-pointer"
            on:click={toggleOpen}
        >
            <div
                class="children:w-5 px-2 transition-transform"
                style="transform: rotate({openArrowDeg}deg);"
            >
                <IconChevronRight />
            </div>
            <div class="grow font-bold uppercase">
                {section.title}
                {#if !open} ({section.tasks.length + 1}) {/if}
            </div>
            {#each [{ label: "Edit", icon: IconEdit, onClick: onEdit }, { label: "Delete", icon: IconTrash, onClick: onDelete }] as it}
                <button
                    class="btn btn-ghost btn-xs h-10 px-3 flex justify-center items-center"
                    on:click|stopPropagation={it.onClick}
                >
                    <svelte:component this={it.icon} />
                    <span>{it.label}</span>
                </button>
            {/each}
        </header>
        <main style="--open-height:{openHeight}px">
            <div
                class="content p-2 flex flex-wrap"
                bind:clientHeight={contentHeght}
            >
                {#each section.tasks as task, inx}
                    <div
                        class="h-24 bg-base-100 m-2 rounded-lg p-4 flex items-center border border-base-300 overflow-y-hidden"
                    >
                        <div
                            class="m-2 mr-3 flex overflow-hidden w-11 h-11 rounded-full shrink-0 border-2 border-primary "
                        >
                            <img
                                width="100%"
                                height="100%"
                                src="https://picsum.photos/seed/picsum/200?random={inx}"
                                alt="user"
                            />
                        </div>
                        <div
                            class="flex flex-col overflow-y-hidden max-h-full mr-3"
                        >
                            <div class="flex items-center">
                                <div
                                    class="text-xs bg-secondary px-2 py-1 rounded mr-2 font-bold"
                                >
                                    Design
                                </div>
                                <div class="text-xs">Date 2022.01.01</div>
                            </div>
                            <div
                                class="flex flex-col px-1 max-w-xs overflow-y-hidden overflow-ellipsis font-bold"
                            >
                                {task.title}
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </main>
    </div>
</div>

<style lang="scss">
    main {
        --open-height: 0;
        overflow: hidden;
        position: relative;
        height: var(--open-height);
        transition: height 300ms ease-in-out;
    }

    main > .content {
        transition: transform 300ms ease-in-out;
        position: absolute;
    }
</style>
