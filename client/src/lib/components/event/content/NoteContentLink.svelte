<script>
	import { isAudio, isImage, isVideo } from '$lib/utils/kind-utils';
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	export let value;
	export let showMedia = false;
</script>

{#if showMedia && value.isMedia}
	{#if !!isImage(value.url)}
		<img class="media" src={value.url} alt={''} />
	{:else if isVideo(value.url)}
		<!-- svelte-ignore a11y-media-has-caption -->
		<video class="media" src={value.url} controls />
	{:else if isAudio(value.url)}
		<audio src={value.url} controls>
			<a href={value.url}>{value.url.replace(/https?:\/\/(www\.)?/, '')}</a>
		</audio>
	{:else}
		<a href={value.url}>
			{value.url.replace(/https?:\/\/(www\.)?/, '')}
		</a>
	{/if}
{:else}
	<a href={value.url}>
		{value.url.replace(/https?:\/\/(www\.)?/, '')}
	</a>
{/if}

<style>
	.media {
		max-width: 100%; /* Ensures it does not exceed the width of its container */
		max-height: 500px; /* Example max-height; adjust as necessary */
		width: auto; /* Maintains aspect ratio */
		height: auto; /* Maintains aspect ratio */
	}
</style>
