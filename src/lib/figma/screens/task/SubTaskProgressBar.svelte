<script lang="ts">
    // between 0 and 1
    export let progress: number;
</script>

<div class="h-2 w-full overflow-hidden rounded bg-disabled">
    <div class="h-full bg-primary" style:width="{progress * 100}%" />
</div>
