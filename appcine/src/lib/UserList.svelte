<script>
// @ts-nocheck

    import User from "./User.svelte";
    import UserUpdate from "./UserUpdate.svelte";
    let user = null;
    let atualizou = false;
    let promise = getUsers();
    let deletou = false;

    async function getUsers() {
        const res = await fetch(`http://localhost:8000/user/list`);
        const text = await res.json();
        if (res.ok) {
            return text;
        } else {
            throw new Error(text);
        }
    }

    function handleClick() {
        promise = getUsers();
    }
    function update() {
        const id = this.getAttribute("id");
        user = id;
        atualizou = true;
    }

    async function deleteUser() {
        const id = this.getAttribute("id");
        const res = await fetch(`http://localhost:8000/user/delete/${id}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        });
        promise = getUsers();
        deletou = true;
        setTimeout(() => {
            deletou = false;
        }, 3000);
    }
</script>

{#await promise}
    <p>...waiting</p>
{:then users}
    {#if atualizou === false}
        {#if deletou}
            <p class="delete">Usuário deletado com sucesso!</p>
        {/if}
        <div class="table">
            {#each users as u}
                <p>{u.id}</p>
                <p>{u.name}</p>
                <p>{u.email}</p>
                <button id={u.id} class="update" on:click={update}
                    >Update</button
                >
                <button id={u.id} class="delete" on:click={deleteUser}
                    >Delete</button
                >
            {/each}
        </div>

        <button on:click={handleClick}>Refresh</button>
    {/if}
{:catch error}
    <p style="color: red">{error.message}</p>
{/await}

{#if atualizou === true}
    <svelte:component this={UserUpdate} usuario={user} />
{/if}

<style>
    .table {
        margin-top: 10px;
        display: grid;
        grid-template-columns: 0.5fr 1fr 1fr 1fr 1fr;
        /* border: 1px solid #ccc; */
        padding: 5px;
    }
    button.delete {
        background-color: #db0000;
        border: none;
        color: white;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 12px;
        margin: 4px 2px 4px 2px;
        cursor: pointer;
    }
    button.delete:hover {
        background-color: #ff0000;
    }
    button.update {
        background-color: #4caf50;
        border: none;
        color: white;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 12px;
        margin: 4px 2px 4px 20px;
        cursor: pointer;
    }
    button.update:hover {
        background-color: #5cb85c;
    }
    p.delete {
        color: #db0000;
    }
</style>
