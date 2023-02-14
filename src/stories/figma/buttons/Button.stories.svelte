<script lang="ts">
    import { Meta, Template, Story } from "@storybook/addon-svelte-csf";
    import Button from "$lib/figma/buttons/Button.svelte";
    import { action } from "@storybook/addon-actions";

    import { Plus } from "@steeze-ui/heroicons";

    import { buttonSizes, buttonColors } from "$lib/figma/types";
    import { fr, fc, falseTrue } from "$lib/storybook";

    const argTypes = {};
</script>

<Meta title="Button" component={Button} {argTypes} />

<Template let:args>
    <div class={fr}>
        {#each buttonColors as color}
            <div class={fc}>
                {#each buttonSizes as size}
                    <div class={fr}>
                        {#each falseTrue as disabled}
                            <Button
                                label="Hello, World"
                                {...args}
                                {color}
                                {size}
                                {disabled}
                                on:click={action("This button was clicked")}
                            />
                        {/each}
                    </div>
                {/each}
            </div>
        {/each}
    </div>
</Template>

<Story name="Primary" args={{ style: { kind: "primary" } }} />

<Story name="Secondary" args={{ style: { kind: "secondary" } }} />

<Story
    name="Tertiary No Icon"
    args={{ style: { kind: "tertiary", icon: null } }}
/>
<Story
    name="Tertiary Icon Left"
    args={{
        style: {
            kind: "tertiary",
            icon: { position: "left", icon: Plus },
        },
    }}
/>
<Story
    name="Tertiary Icon Right"
    args={{
        style: {
            kind: "tertiary",
            icon: {
                position: "right",
                icon: Plus,
            },
        },
    }}
/>
