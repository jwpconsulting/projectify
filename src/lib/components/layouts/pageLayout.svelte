<script lang="ts">
    export let headerMode: string | undefined = undefined;
</script>

<p>Dont use me</p>
<p>
    headermode: {headerMode}
</p>
<div class="h-40 w-40 overflow-hidden">
    <slot />
</div>
<p>Dont use me</p>
