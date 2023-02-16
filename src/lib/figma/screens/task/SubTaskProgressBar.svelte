<script lang="ts">
    // between 0 and 100
    export let progress: number;

    let width: string;
    $: {
        if (progress < 0 || progress > 100) {
            throw new Error(
                `Progress must be between 0 and 100. Given: ${progress}`
            );
        }
        width = `${progress}%`;
    }
</script>

<div class="h-2 w-full overflow-hidden rounded bg-disabled">
    <div class="h-full bg-primary" style:width />
</div>
