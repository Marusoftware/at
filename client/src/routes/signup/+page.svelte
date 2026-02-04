<script lang="ts">
	import { AuthService } from "$lib/openapi";
    import Button from "flowbite-svelte/Button.svelte";
    import Card from "flowbite-svelte/Card.svelte";
    import Heading from "flowbite-svelte/Heading.svelte";
    import Input from "flowbite-svelte/Input.svelte";
    import Label from "flowbite-svelte/Label.svelte";
    import A from "flowbite-svelte/A.svelte";
    import Stepper from "flowbite-svelte/DetailedStepper.svelte"
	import { goto } from "$app/navigation";
	import type { DetailedStep } from "flowbite-svelte"
    
    let mail=$state("");
    let current_step=$state(1);
    const steps:DetailedStep[] = [
        {id:1, label:"Email", description:"Select account Email address"},
        {id:2, label:"Verification"},
    ]
    const onSubmit=async (e:SubmitEvent) => {
        e.preventDefault()
        await AuthService.authSignup({body:{mail}});
        mail="";
        goto("/signin");
    }
</script>

<Card class="mx-auto p-8">
    <Heading tag="h3">サインアップ</Heading>
    <Stepper steps={steps} bind:current={current_step} clickable={false} />
    <form onsubmit={onSubmit} class="space-y-2 flex flex-col">
            <Label for="mail">Email Address</Label>
            <Input id="mail" type="email" bind:value={mail} autocomplete="email" required />
            <Button type="submit">Sign up</Button>
    </form>
    <p>すでにアカウントをお持ちの方は<A href="/signin">こちら</A></p>
</Card>