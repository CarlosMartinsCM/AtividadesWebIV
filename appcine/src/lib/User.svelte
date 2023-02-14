<script>
    import UserList from "./UserList.svelte";

    let resposta = "";
    let cadastrou = false;
    async function sendForm(e) {
        // envia o formulario no formato json
        let formData = new FormData(e.target);
        let data = Object.fromEntries(formData.entries());
        cadastrou = true;
        const res = await fetch("http://localhost:8000/user/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        const json = await res.json();
        resposta = JSON.stringify(json);
    }
</script>

{#if cadastrou === false}
    <h2>New user</h2>
    <form class="crud" on:submit|preventDefault={sendForm}>
        <input
            type="text"
            name="name"
            placeholder="User name"
            required
            autocomplete="off"
        />
        <input
            type="text"
            name="email"
            placeholder="Email"
            required
            autocomplete="off"
        />
        <input
            type="text"
            name="password"
            placeholder="password"
            required
            autocomplete="off"
        />
        <input type="submit" value="add" />
    </form>
{/if}

{#if cadastrou === true}
    <svelte:component this={UserList} />
{/if}

<style>
    form.crud {
        display: grid;
        grid-template-columns: 1fr;
        gap: 5px;
        row-gap: 10px;
    }
    .crud input[type="submit"] {
        justify-self: baseline;
    }
</style>
