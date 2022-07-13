<script context="module" lang="ts">
    export type DropDownMenuItem = {
        id?: any;
        label: string;
        icon: any;
        onClick?: (...arg0: any) => void;
        href?: string;
        disabled?: boolean;
        hidden?: boolean;
        tooltip?: string;
        items?: DropDownMenuItem[];
        open?: boolean;
    };

    type DropDown = {
        open: (...arg0: any[]) => void;
        openComponent: (...arg0: any[]) => void;
        close: (...arg0: any[]) => void;
    };

    let dropDown: DropDown | null = null;

    export function getDropDown(): DropDown | null {
        return dropDown;
    }
</script>

<script lang="ts">
    import { SvelteComponent, tick } from "svelte";
    import IconChevronDown from "./icons/icon-chevron-down.svelte";

    let component: SvelteComponent | null = null;
    let componentProps: any | null = null;
    let items: DropDownMenuItem[] | null = null;
    let target: HTMLElement | null = null;
    let focusEl: HTMLElement | null = null;
    let activeId: any | null = null;
    let rootEl: HTMLElement | null;
    let startX: number;
    let startY: number;
    let x: number;
    let y: number;

    let ofX = 0;
    let ofY = 0;

    let posMargin = 4;

    function checkTargetPosition() {
        if (!target) {
            return;
        }
        if (!rootEl) {
            throw new Error("Expected rootEl");
        }
        if (!rootEl.parentElement) {
            throw new Error("Expected rootEl.parentElement");
        }

        const rect = target.getBoundingClientRect();
        const newX = Math.round(rect.left);
        const newY = Math.round(rect.top);

        if (Math.abs(startX - newX) > 10 || Math.abs(startY - newY) > 10) {
            close();
            return;
        }

        const viewPortRect = rootEl.parentElement.getBoundingClientRect();
        const menuRect = rootEl.getBoundingClientRect();

        ofY = rect.height + posMargin;
        ofX = rect.width - menuRect.width;

        x = newX + ofX;
        y = newY + ofY;

        let deltaBottom =
            y + menuRect.height - viewPortRect.bottom + posMargin;

        if (deltaBottom > 0) {
            y -= deltaBottom;
        }

        if (x - posMargin < 0) {
            x = posMargin;
        }

        window.requestAnimationFrame(checkTargetPosition);
    }

    async function placeDialog() {
        await tick();

        if (!focusEl) {
            throw new Error("Expected focusEl");
        }
        if (!target) {
            throw new Error("Expected target");
        }
        focusEl.focus();
        const rect = target.getBoundingClientRect();
        startX = Math.round(rect.left);
        startY = Math.round(rect.top);

        checkTargetPosition();
        window.requestAnimationFrame(checkTargetPosition);
    }

    async function open(
        its: DropDownMenuItem[],
        trg: HTMLElement,
        aId: any = null
    ) {
        close();
        items = its;
        target = trg;
        activeId = aId;
        placeDialog();
    }

    async function openComponent(
        comp: SvelteComponent,
        trg: HTMLElement,
        props: any
    ) {
        close();
        target = trg;
        component = comp;
        componentProps = props;
        placeDialog();
    }

    function close() {
        items = null;
        target = null;
        component = null;
        componentProps = null;
    }

    dropDown = { open, openComponent, close };
</script>

{#if items || component}
    <div
        style={`top:${y}px; left:${x}px;`}
        bind:this={rootEl}
        class="absolute z-50 select-none"
    >
        {#if component}
            <div
                bind:this={focusEl}
                tabindex="0"
                on:blur={(e) => {
                    if (!e.relatedTarget) {
                        throw new Error("Expected e.relatedTarget");
                    }
                    if (!focusEl) {
                        throw new Error("Expected focusEl");
                    }
                    if (!(e.relatedTarget instanceof HTMLElement)) {
                        throw new Error("e.relatedTarget not HTMLElement");
                    }
                    if (!focusEl.contains(e.relatedTarget)) {
                        close();
                    }
                }}
            >
                <svelte:component
                    this={component}
                    {...componentProps}
                    on:{console.log}
                />
            </div>
        {:else if items}
            <ul
                bind:this={focusEl}
                on:blur={(e) => {
                    if (!e.relatedTarget) {
                        throw new Error("Expected e.relatedTarget");
                    }
                    if (!focusEl) {
                        throw new Error("Expected focusEl");
                    }
                    if (!(e.relatedTarget instanceof HTMLElement)) {
                        throw new Error("e.relatedTarget not HTMLElement");
                    }
                    if (!focusEl.contains(e.relatedTarget)) {
                        close();
                    }
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
                                class="h-9 space-x-2 truncate px-0 text-xs font-bold"
                                href={it.href}
                                on:click={() => {
                                    if (!it.items) {
                                        if (it.onClick) {
                                            it.onClick();
                                        }
                                        if (!focusEl) {
                                            throw new Error(
                                                "Expected focusEl"
                                            );
                                        }
                                        focusEl.blur();
                                        close();
                                    } else {
                                        it.open = !it.open;
                                    }
                                }}
                            >
                                <svelte:component this={it.icon} />
                                <span class="grow">{it.label}</span>

                                {#if it.items}
                                    <div
                                        class:rotate-180={it.open}
                                        class="icon-sm transition-all"
                                    >
                                        <IconChevronDown />
                                    </div>
                                {/if}
                            </a>

                            {#if it.items}
                                <ul
                                    class:h-0={!it.open}
                                    class="menu overflow-hidden pl-0"
                                >
                                    {#each it.items || [] as it}
                                        <li>
                                            <a
                                                title={it.tooltip}
                                                disabled={it.disabled}
                                                class:active={activeId ===
                                                    it.id}
                                                class="nowrap-ellipsis h-9 space-x-2 px-0 text-xs font-bold"
                                                href={it.href}
                                                on:click={() => {
                                                    if (!focusEl) {
                                                        throw new Error(
                                                            "Expected focusEl"
                                                        );
                                                    }
                                                    if (it.onClick) {
                                                        it.onClick();
                                                    }
                                                    focusEl.blur();
                                                }}
                                            >
                                                <svelte:component
                                                    this={it.icon}
                                                />
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
        {/if}
    </div>
{/if}
