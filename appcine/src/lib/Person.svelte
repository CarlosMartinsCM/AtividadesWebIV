<script>
    // import { is_empty } from "svelte/internal";

    let formatDate = (date) => {
        var d = new Date(date),
            month = "" + (d.getMonth() + 1),
            day = "" + d.getDate(),
            year = d.getFullYear();
        if (month.length < 2) month = "0" + month;
        if (day.length < 2) day = "0" + day;
        return [day, month, year].join("/");
    };

    let person_name = null;
    let person = null;
    let message = null;
    async function getPerson() {
        const res = await fetch(
            `http://localhost:8000/artist/name/${person_name}`
        );
        const data = await res.json();
        if (res.ok) {
            person = data;
            message = null;
        } else {
            person = null;
            message = `ID ${person} ${res.statusText}`;
        }
    }
</script>

<input
    class="input"
    bind:value={person_name}
    type="text"
    placeholder="Digite o nome do artista"
/>
<button class="botao1" on:click={getPerson}> Buscar </button>

<div class="table">
    <section>
        {#if person !== null}
            <img
                class="img"
                src="https://image.tmdb.org/t/p/w185{person['imagem']}"
                alt="Imagem do artista"
                height="200"
                width="200"
            />
            <h1>{person.nome}</h1>
            <div class="info">
                <ul class="lista">
                    <li>ID: {person.id}</li>
                    <li>Data de Nascimento: {formatDate(person.birthday)}</li>
                    <li>Local de Nascimento: {person.local_nascimento}</li>
                    <li>Popularidade: {person.popularidade}</li>
                </ul>
            </div>
            <div class="bio">
                <h3>Biografia</h3>
                <p>{person.biografia}</p>
            </div>
        {:else if message !== null}
            <p class="error">{message}</p>
        {/if}
    </section>
</div>

<style>
    .img {
        width: 17%;
        /* 100% da imagem*/
        border-radius: 50%;
        margin-top: 50px;
    }

    .info {
        text-align: left;
        border: 1px solid black;
        border-radius: 10px;
    }

    .bio {
        text-align: left;
        border: 1px solid black;
        border-radius: 10px;
        margin-top: 10px;
        padding: 10px 10px 10px;
    }

    .lista {
        list-style-type: none;
        padding: 10px 10px 10px;
        font-size: 18pt;
    }
    .botao1 {
        border: 1px solid black;
        border-radius: 10px;
        color: white;
        background-color: rgb(29, 71, 33);
    }
    .input {
        border: 0.05px solid black;
        width: 300px;
        height: 30px;
        border-radius: 10px;
        font-size: 14pt;
    }
</style>
