<script lang="ts">
    import Button from "$lib/figma/Button.svelte";
    import { Plus } from "@steeze-ui/heroicons";
    import { buttonStyles, buttonSizes, buttonColors } from "$lib/figma/types";
    import type { ButtonIcon } from "$lib/figma/types";

    const buttonTertiares: ButtonIcon[] = [
        { position: "left", icon: Plus },
        { position: "right", icon: Plus },
        null,
    ];
    const disabledStates = [true, false];
</script>

<div class="flex flex-col flex-wrap gap-2">
    <div class="flex flex-row flex-wrap">
        Buttons
        {#each buttonStyles as style}
            <div class="flex flex-col flex-wrap">
                <div class="capitalize">
                    {style}
                </div>
                {#each buttonColors as color}
                    <div class="flex flex-col flex-wrap">
                        <div class="capitalize">
                            {color}
                        </div>
                        {#each buttonSizes as size}
                            <div class="flex flex-row flex-wrap items-center">
                                {#if style == "tertiary"}
                                    {#each buttonTertiares as icon}
                                        <div class="capitalize">
                                            {icon ? icon.position : "no"}
                                        </div>
                                        <Button
                                            on:click={console.log}
                                            {style}
                                            {size}
                                            {color}
                                            disabled={false}
                                            {icon}
                                        >
                                            Button
                                        </Button>
                                    {/each}
                                {:else}
                                    {#each disabledStates as disabled}
                                        <Button
                                            on:click={console.log}
                                            {style}
                                            {size}
                                            {color}
                                            {disabled}
                                            icon={null}
                                        >
                                            {disabled ? "Disabled" : "Button"}
                                        </Button>
                                    {/each}
                                {/if}
                            </div>
                        {/each}
                    </div>
                {/each}
            </div>
        {/each}
    </div>
</div>
