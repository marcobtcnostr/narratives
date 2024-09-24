<!-- src\lib\components\carousel\GenericCarousel.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';

	import ChevronRightIcon from '$lib/components/icons/ChevronRightIcon.svelte';
	import ChevronLeftIcon from '$lib/components/icons/ChevronLeftIcon.svelte';

	export let images = [];
	export let components = [];
	export let dataStore;
	let currentPosition = 0; // Start with the first item

	// Function to go to the next set of items
	function next() {
		currentPosition = (currentPosition + 1) % (images.length + components.length); // Loop back to start
	}

	// Function to go to the previous set of items
	function prev() {
		currentPosition =
			(currentPosition - 1 + images.length + components.length) %
			(images.length + components.length); // Loop back to end
	}

	// A reactive statement to calculate the position, size, and height of each card based on the current position
	$: cardStyles = [...images, ...components].map((_, index) => {
		let positionIndex =
			(index - currentPosition + images.length + components.length) %
			(images.length + components.length);
		let width = positionIndex === 1 ? '50%' : '25%';
		let zIndex = positionIndex === 1 ? '2' : '1';
		let xPosition = positionIndex === 1 ? '-50%' : positionIndex === 0 ? '-98%' : '-2%';
		let height = positionIndex === 1 ? '200px' : '150px'; // Central item has 200px height, others have 150px

		return `width: ${width}; z-index: ${zIndex}; height: ${height}; transform: translateX(${xPosition}) translateX(${(positionIndex - 1) * 100}%);`;
	});
</script>

<div class="carousel">
	<ul class="cards">
		<!-- {#each images as image, index (image.id)}
			<li style={cardStyles[index]}>
				<img src={image.src} alt={image.alt} />
			</li>
		{/each} -->
		{#each components as component, index (component.id)}
			<li class="component-container" style={cardStyles[images.length + index]}>
				<svelte:component this={component.component} dataStore={dataStore}/>
			</li>
		{/each}
	</ul>
	<div class="actions">
		<button class="prev" on:click={prev}>
			<ChevronLeftIcon />
		</button>
		<button class="next" on:click={next}>
			<ChevronRightIcon />
		</button>
	</div>
</div>

<style>
	.carousel {
		position: relative;
		width: 100%;
		height: auto;
		overflow: hidden;
	}

	.cards {
		display: flex;
		transition: transform 0.5s ease;
		will-change: transform; /* Optimizes for animations */
		padding: 0;
		position: relative;
		height: 200px !important;
		margin: 0px;
		/* margin-top: 20px; */
		/* margin-bottom: 20px; */
		width: 100%;
	}

	.cards li {
		list-style: none;
		padding: 0;
		margin: 0;
		position: absolute;
		left: 50%;
		text-align: center;
		border-radius: 0.8rem;
		transition:
			transform 0.5s ease,
			width 0.5s ease;
	}

	.cards img {
		width: 100%;
		height: auto;
		object-fit: cover;
		border-radius: 0.8rem;
	}

	.actions {
		position: absolute;
		left: 50%; /* Align the left edge of the button container with the center of the carousel */
		transform: translateX(-50%); /* Center the button container horizontally */
		bottom: 0;
		width: 100%;
		display: flex;
		justify-content: space-between;
		padding: 0 10px;
		margin-bottom: 15px;
	}

	.actions button {
		background-color: transparent;
		border: none;
		color: var(--color-text);
		height: 50px;
	}

	.component-container {
		width: 100%;
		height: 200px;
		display: flex;
		justify-content: center;
		align-items: center;
		overflow: hidden;
	}

	/* Style adjustments for component resizing, if necessary */
	.component-container > * {
		max-height: 100%;
		/* Additional styling to ensure content fits, e.g., object-fit for images */
	}
</style>
