<!-- src\lib\components\user\Avatar.svelte -->

<script lang="ts">
	import { onMount } from 'svelte';

	export let ndk: any;
	export let npub: string | undefined = undefined;
	export let pubkey: string | undefined = undefined;
	export let user: any = undefined;
	export let userProfile: any = undefined;

	if (!userProfile && !user) {
		let opts = npub ? { npub } : { pubkey };
		try {
			user = ndk?.getUser(opts);
		} catch (e) {
			console.error(`error trying to get user`, { opts }, e);
		}
	}

	const fetchProfilePromise = new Promise((resolve, reject) => {
		if (userProfile) {
			resolve(userProfile);
		} else if (user) {
			user.fetchProfile({
				closeOnEose: true,
				groupable: true,
				groupableDelay: 200,
			}).then(() => {
				userProfile = user.profile;
				if (!userProfile) {
					reject(`no profile`);
				} else {
					resolve(userProfile);
				}
			}).catch(reject);
		} else {
			reject(`no user`);
		}
	});
</script>

{#await fetchProfilePromise}
    <img alt="" class="event-card-avatar event-card-avatar--loading {$$props.class}" style={$$props.style} />
{:then userProfile}
    <img
        src={userProfile?.image ?? ""}
        alt=""
        class="event-card-avatar event-card-avatar--image {$$props.class}"
        style={$$props.style}
    />
{:catch error}
    <img
        alt=""
        class="event-card-avatar event-card-avatar--error {$$props.class}"
        data-error={error}
        style={$$props.style}
    />
{/await}

<style lang="postcss">
</style>
