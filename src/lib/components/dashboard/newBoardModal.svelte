<script lang="ts">
    import { getContext } from "svelte";

    let boardName = "";
    const modal = getContext<any>("modal");
    function submit() {
        modal.close({ boardName });
    }
</script>

<div class="card-body items-center">
    <div class="form-control w-full">
        <label for="boardName" class="label label-text">BoardName</label>
        <input
            type="text"
            name="boardName"
            placeholder="boardName"
            class="input input-bordered"
            bind:value={boardName}
        />
    </div>
    <div class="pt-7">
        <button class="btn btn-primary" on:click={submit}>Create</button>
    </div>
</div>
