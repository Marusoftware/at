<script lang="ts">
    let { digits = 1, value = $bindable("") }: {digits?:number, value?: string} = $props();
    let input_elements = $state<HTMLInputElement[]>([]);
    const handleInput = (i:number) => {
        try {
            if (!Number.isInteger(Number(input_elements[i].value)))
            {
                throw Error;
            }
        } catch (e) {
            input_elements[i].value = "";
            return;
        }
        if (input_elements[i].value.length === 1 && i+1 < input_elements.length)
        {
            input_elements[i+1].focus();
        }
        else if (input_elements[i].value.length === 0 && i !== 0)
        {
            input_elements[i-1].focus();
        }
        let output_string = "";
        for (const input_element of input_elements)
        {
            if (input_element.value.length !== 1)
            {
                return;
            }
            output_string+=input_element.value;
        }
        value=output_string;
    }
    const handleBackspace = (e:KeyboardEvent, i:number) => {
        if (e.key === "Backspace" && input_elements[i].value.length === 0)
        {
            handleInput (i);
        }
    }
    
</script>

<fieldset class="mx-auto flex mb-2 space-x-2 rtl:space-x-reverse">
    {#each { length:digits }, i }
        <input oninput={()=>handleInput(i)} 
               onkeyup={(e)=>handleBackspace(e, i)}
               bind:this={input_elements[i]} 
               type="text" maxlength="1"
               defaultValue={value[i]??""}
               class="text-center block w-full focus:outline-hidden border border-gray-300 dark:border-gray-600 focus:border-primary-500 focus:ring-primary-500 dark:focus:border-primary-500 dark:focus:ring-primary-500 bg-gray-50 text-gray-900 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 bg-gray-50 text-gray-900 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 rounded" required />
    {/each}
</fieldset>
<!-- <p id="helper-text-explanation" class="mt-2.5 text-sm text-body">Please introduce the 6 digit code we sent via email.</p> -->