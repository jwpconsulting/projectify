<script lang="ts">
    import { getContext } from "svelte";
    import { _ } from "svelte-i18n";

    let boardName = "";
    const modal = getContext<any>("modal");
    function submit() {
        modal.close({ boardName });
    }
</script>

<div class="card-body items-center">
    <div class="form-control w-full">
        <label for="boardName" class="label label-text"
            >{$_("board-name")}</label
        >
        <input
            type="text"
            name="boardName"
            placeholder="boardName"
            class="input input-bordered"
            bind:value={boardName}
        />
    </div>
    <div class="pt-7">
        <button class="btn btn-primary" on:click={submit}
            >{$_("create")}</button
        >
    </div>
</div>
