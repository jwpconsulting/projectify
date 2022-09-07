<script lang="ts">
    import InputField from "$lib/figma/InputField.svelte";
    import { inputFieldStyles, inputFieldSizes } from "$lib/figma/types";
    import { fc, fr } from "$lib/storybook";
</script>

<div class={fc}>
    {#each inputFieldSizes as size}
        <div class={fr}>
            <div class="capitalize">
                {size}
            </div>
            <div class={fc}>
                {#each inputFieldStyles as style}
                    <div class={fr}>
                        <div class="capitalize">
                            {style}
                        </div>
                        <div class="w-96">
                            <InputField {style} placeholder="Enter input" />
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    {/each}
</div>
