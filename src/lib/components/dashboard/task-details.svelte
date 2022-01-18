<script>
    import { currenTaskDetailsUUID } from "$lib/stores/dashboard";
    import IconPlus from "../icons/icon-plus.svelte";
</script>

<div class="flex flex-col p-0 w-[60vw]">
    <header class="flex p-6 space-x-4 items-center bg-base-100">
        <div
            class="flex justify-center items-center overflow-hidden w-11 h-11 rounded-full shrink-0 border-2 border-primary text-primary border-dashed hover:ring"
        >
            <IconPlus />
        </div>

        <input class="grow text-xl p-2 rounded-md" placeholder="Task Name" />

        <button class="btn btn-primary rounded-full">Save</button>
    </header>
    <div class="tabs px-6">
        <button class="tab tab-bordered tab-active">Tasks</button>
        <button class="tab tab-bordered">Discussion</button>
        <div class="h-[2px] grow bg-base-300" />
    </div>
    <main class="flex flex-col overflow-y-auto">
        <div class="flex flex-col p-6 space-y-4">
            <div class="text-xl uppercase font-bold">Overview</div>
            <textarea
                rows="6"
                class="textarea textarea-bordered resize-none leading-normal p-4"
                placeholder="Please enter an overview"
            />
        </div>
        <div class="flex flex-col p-6 space-y-4">
            <div class="flex text-xl space-x-2">
                <span class=" uppercase font-bold">Sub Task</span>
                <span>0%</span>
            </div>

            <progress class="progress progress-primary" value="50" max="100" />

            <div>
                {#each [1, 2, 3, 4, 1, 2, 3, 41, 2, 3, 4] as it}
                    <label class="cursor-pointer label space-x-2">
                        <input
                            type="checkbox"
                            checked
                            class="checkbox checkbox-primary"
                        />
                        <div class="grow">Button desing</div>
                    </label>
                {/each}
            </div>
        </div>
    </main>
</div>

<style lang="scss">
    main {
        max-height: calc(100vh - 128px);
    }
</style>
