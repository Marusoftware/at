<script lang="ts">
	import { type PageData } from "./$types";
    import Heading from "flowbite-svelte/Heading.svelte"
    import Card from "flowbite-svelte/Card.svelte"
    import Button from "flowbite-svelte/Button.svelte"

    export let data:PageData;

    const user=data.user;
    
</script>

<Heading tag="h3">Welcome to @Marusoftware</Heading>
{#if $user}
aaaa
{:else}
<Card class="mx-auto space-y-2 p-4">
    <Button href="/signin">Signin</Button>
    <Button href="/signup">Signup</Button>
</Card>
{/if}