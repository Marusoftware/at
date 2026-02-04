import { showNotification } from "$lib/notification";
import { AuthService, type Token } from "$lib/openapi";
import { client } from "$lib/openapi/client.gen";
import { writable, get } from "svelte/store";

export const prerender = true
export const ssr = false

const user = writable<Token|undefined>(undefined);

export const load = async ()=>{
    client.setConfig({baseUrl:"/api/v1", auth:()=>"Bearer "+get(user)?.access_token, headers:{accept:"application/json"}, throwOnError:false})
    try {
        const token = await AuthService.authSession();
        if(token.data && token.data.length>=1){
            user.set(token.data[0]);
            showNotification({title: 'Login Successfull!', kind:'info'})
        }
    } catch(e){
        console.debug("auth error")
        const token=undefined;
    }
    client.interceptors.response.use(async (response, request, options) => {
        if (!response.ok) {
            const body=await response.json()
            showNotification({title:'Error', kind:'warn', subtitle: body.detail})
        }
        return response
    })
    return {user}
}