<script lang="ts">
    export let content = "";
    export let placeholder = "";
    export let modified = false;
    let editMode = false;
    import { tick } from "svelte";
    let textAreaEl: HTMLElement;

    function urlify(text: string) {
        var urlRegex = /(https?:\/\/[^\s]+)/g;
        return text.replace(urlRegex, function (url) {
            return '<a href="' + url + '" target="_blank">' + url + "</a>";
        });
    }

    function transform(text: string) {
        text = urlify(text);
        text = text.replace(/\n/g, "<br>");
        return text;
    }
</script>

<textarea
    bind:this={textAreaEl}
    class:hidden={!editMode}
    rows="6"
    class="textarea textarea-bordered resize-none p-4 leading-normal"
    {placeholder}
    on:input={() => (modified = true)}
    on:blur={() => (editMode = false)}
    bind:value={content}
/>
<div
    class:hidden={editMode}
    class="rich-textarea textarea textarea-bordered h-40 overflow-y-auto p-4 leading-normal"
    on:click={async () => {
        editMode = true;
        await tick();
        textAreaEl.focus();
    }}
>
    {#if content}
        {@html transform(content)}
    {:else}
        <div class="placeholder">{placeholder}</div>
    {/if}
</div>
