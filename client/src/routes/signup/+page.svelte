<script lang="ts">
	import { AuthService } from "$lib/openapi";
    import Button from "flowbite-svelte/Button.svelte";
    import Card from "flowbite-svelte/Card.svelte";
    import Heading from "flowbite-svelte/Heading.svelte";
    import Input from "flowbite-svelte/Input.svelte";
    import Label from "flowbite-svelte/Label.svelte";
    import A from "flowbite-svelte/A.svelte";
	import { goto } from "$app/navigation";
    
    let username=$state("");
    let password=$state("");
    let mail=$state("");
    const onSubmit=async (e:SubmitEvent) => {
        e.preventDefault()
        await AuthService.authSignup({body:{name:username, password, mail}});
        username="";
        password="";
        mail="";
        goto("/signin");
    }
</script>

<Card class="mx-auto p-8">
    <Heading tag="h3">サインアップ</Heading>
    <form onsubmit={onSubmit} class="space-y-2 flex flex-col">
            <Label for="username">User Name</Label>
            <Input id="username" type="text" bind:value={username} required />
            <Label for="mail">Email Address</Label>
            <Input id="mail" type="email" bind:value={mail} required />
            <Label for="password">Password</Label>
            <Input id="password" type="password" bind:value={password} required />
            <Button type="submit">Sign up</Button>
    </form>
    <p>すでにアカウントをお持ちの方は<A href="/signin">こちら</A></p>
</Card>