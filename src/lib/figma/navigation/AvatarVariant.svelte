<script lang="ts">
    import AvatarState from "$lib/figma/navigation/AvatarState.svelte";
    import type {
        AvatarStateSize,
        AvatarVariantContent,
    } from "$lib/figma/types";

    export let content: AvatarVariantContent;
    export let size: AvatarStateSize;
</script>

<div class="p-0.5">
    <AvatarState user={content.user} {size} />
</div>
