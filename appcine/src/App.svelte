<script>
  import Movie from './lib/Movie.svelte'
  import User from './lib/User.svelte'
  import Person from './lib/Person.svelte'
  import UserList from './lib/UserList.svelte';
  let menu = 1;
</script>

<main class='container'>
    <p>Projeto Web IV</p>
    
    <ul class="nav">
        <li class="botao"><a href="/" on:click|preventDefault={() => (menu = 1)}>Cadastrar Usuário</a></li>
        <li class="botao"><a href="/" on:click|preventDefault={() => (menu = 11)}>Listar Users</a></li>
        <li class="botao"><a href="/" on:click|preventDefault={() => (menu = 2)}>Movies</a></li>
        <li class="botao"><a href="/" on:click|preventDefault={() => (menu = 3)}>Artista</a></li>
    </ul>

    <div class="card">
    {#if menu === 1}
        <User/>
    {:else if menu === 11}
        <UserList/>
    {:else if menu === 2}
        <Movie/>
    {:else if menu === 3}
        <Person/>
    {:else}
        <p>invalid option</p>
    {/if}
    </div>
</main>

<style>

ul.nav {
    display: flex;
    padding: 0;
    place-content: center;
    
}
ul.nav li{
    display: inline-block;
    padding: 0px 5px;
}
.botao {
    border: 1px solid black;
    padding: 10;
}
</style>