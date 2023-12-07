<script lang="ts">
    import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
    import { falseTrue, fc, fr, users } from "$lib/storybook";
</script>

Filter user avatar
<div class={fc}>
    {#each users as user}
        <div class={fr}>
            {#each falseTrue as active}
                <SelectUserClosedNav {active} {user} />
            {/each}
        </div>
    {/each}
</div>
