<script lang="ts">
	import { AuthService } from "$lib/openapi";
    import Button from "flowbite-svelte/Button.svelte";
    import Card from "flowbite-svelte/Card.svelte";
    import Heading from "flowbite-svelte/Heading.svelte";
    import Input from "flowbite-svelte/Input.svelte";
    import Label from "flowbite-svelte/Label.svelte";
    import A from "flowbite-svelte/A.svelte";
	import type { PageData } from "./$types";
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { showNotification } from "$lib/notification";
    export let data:PageData;

    const user=data.user;
    let username="";
    let password="";
    const onSubmit=async (e:SubmitEvent) => {
        e.preventDefault()
        const token=await AuthService.authSignin({body:{username,password}})
        user.set(token.data);
        username="";
        password="";
        showNotification({title:"Login Successful!", kind:"info"})
        goto("/");
    }
    onMount(async () => {
        if($user){
            goto("/");
        }
    })
</script>

<Card class="mx-auto p-8">
    <Heading tag="h3">サインイン</Heading>
    <form on:submit={onSubmit} class="space-y-2 flex flex-col">
            <Label for="username">User Name or Email Address</Label>
            <Input id="username" type="text" bind:value={username} required />
            <Label for="password">Password</Label>
            <Input id="password" type="password" bind:value={password} required />
            <Button type="submit">Sign in</Button>
    </form>
    <p>まだアカウントをお持ちでない方は<A href="/signup">こちら</A></p>
</Card>