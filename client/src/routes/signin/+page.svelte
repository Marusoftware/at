<script lang="ts">
	import { AuthService, type Forbidden } from "$lib/openapi";
    import Button from "flowbite-svelte/Button.svelte";
    import Card from "flowbite-svelte/Card.svelte";
    import Heading from "flowbite-svelte/Heading.svelte";
    import Input from "flowbite-svelte/Input.svelte";
    import Label from "flowbite-svelte/Label.svelte";
    import A from "flowbite-svelte/A.svelte";
    import PinInput from "$lib/components/PinInput.svelte";
	import type { PageProps } from "./$types";
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { showNotification } from "$lib/notification";
    let { data }:PageProps = $props();

    const user=data.user;
    let username=$state("");
    let password=$state("");
    let loading=$state(false);
    let otp_required=$state(false);
    let otp_code=$state("");
    const onSubmit=async (e:SubmitEvent) => {
        e.preventDefault()
        loading=true;
        try {
            const token=await AuthService.authSignin({body:{username,password}});
            user.set(token.data);
            username="";
            password="";
            loading=false;
            showNotification({title:"Login Successful!", kind:"info"})
            goto("/");
        }
        catch (e)
        {
            console.log(e)
            loading=false;
        }
    }
    onMount(async () => {
        if($user){
            goto("/");
        }
    })
</script>

<Card class="mx-auto p-8">
    <Heading tag="h3">サインイン</Heading>
    <form onsubmit={onSubmit} class="space-y-2 flex flex-col">
            <Label for="username">User Name or Email Address</Label>
            <Input id="username" type="text" bind:value={username} required autocomplete="username webauthn"/>
            <Label for="password">Password</Label>
            <Input id="password" type="password" bind:value={password} required autocomplete="current-password webauthn" />
            {#if otp_required}
            <Label id="otp_token" for="otp_token">Password</Label>
            <PinInput digits={6} bind:value={otp_code} />
            {/if}
            <Button loading={loading} type="submit">Sign in</Button>
    </form>
    <p>まだアカウントをお持ちでない方は<A href="/signup">こちら</A></p>
</Card>