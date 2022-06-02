<script context="module" lang="ts">
    let dropDown = null;

    export function getDropDown() {
        return dropDown;
    }
</script>

<script lang="ts">
    import { offsetLimitPagination } from "@apollo/client/utilities";

    import { tick } from "svelte";

    let items = null;
    let target: HTMLElement = null;
    let focusEl;
    let activeId: any = null;
    let rootEl;
    let x, y;

    let ofX = 0;
    let ofY = 0;

    let posMargin = 4;

    function checkTargetPosition() {
        if (!target) {
            return;
        }

        const rect = target.getBoundingClientRect();
        const newX = Math.round(rect.left);
        const newY = Math.round(rect.top);

        if (Math.abs(x - newX) > 10 || Math.abs(y - newY) > 10) {
            close();
            return;
        }

        const menuRect = rootEl.getBoundingClientRect();
        ofY = rect.height + posMargin;
        ofX = rect.width - menuRect.width;

        window.requestAnimationFrame(checkTargetPosition);
    }

    async function open(its, trg) {
        items = its;
        target = trg;

        await tick();

        focusEl.focus();
        const rect = target.getBoundingClientRect();
        x = Math.round(rect.left);
        y = Math.round(rect.top);

        checkTargetPosition();

        window.requestAnimationFrame(checkTargetPosition);
    }

    function close() {
        items = null;
        target = null;
    }

    dropDown = { open, close, items, target };
</script>

{#if items}
    <div
        style={`top:${y + ofY}px; left:${x + ofX}px;`}
        bind:this={rootEl}
        class="absolute select-none"
    >
        <ul
            bind:this={focusEl}
            on:blur={() => {
                console.log("blur");
                close();
            }}
            tabindex="0"
            class="dropdown-content menu min-w-[200px] rounded-lg
        border border-base-300 bg-base-100 py-2 shadow-xl"
        >
            {#each items as it}
                {#if !it.hidden}
                    <li>
                        <a
                            title={it.tooltip}
                            disabled={it.disabled}
                            class:active={activeId === it.id}
                            class="nowrap-ellipsis h-9 space-x-2 px-0 text-xs font-bold"
                            href={it.href}
                            on:click={() => {
                                if (!it.items) {
                                    if (it.onClick) {
                                        it.onClick();
                                    }
                                    focusEl.blur();
                                } else {
                                    it.open = !it.open;
                                }
                            }}
                        >
                            <svelte:component this={it.icon} />
                            <span>{it.label}</span>
                        </a>

                        {#if it.items}
                            <ul class:h-0={!it.open} class="overflow-hidden">
                                {#each it.items as it}
                                    <li>
                                        <a
                                            title={it.tooltip}
                                            disabled={it.disabled}
                                            class:active={activeId === it.id}
                                            class="nowrap-ellipsis h-9 space-x-2 px-0 text-xs font-bold"
                                            href={it.href}
                                            on:click={() => {
                                                if (it.onClick) {
                                                    it.onClick();
                                                }
                                                focusEl.blur();
                                            }}
                                        >
                                            <svelte:component this={it.icon} />
                                            <span>{it.label}</span>
                                        </a>
                                    </li>
                                {/each}
                            </ul>
                        {/if}
                    </li>
                {/if}
            {/each}
        </ul>
    </div>
{/if}
