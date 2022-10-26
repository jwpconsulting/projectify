<script lang="ts">
    export let title: string;
    export let action: () => Promise<void>;
</script>

<form class="flex flex-col gap-12 p-3" on:submit|preventDefault={action}>
    <div class="text-center text-4xl font-bold">
        {title}
    </div>
    <slot />
</form>
