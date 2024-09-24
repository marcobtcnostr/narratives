<!-- src\lib\components\modals\LoginWindow.svelte -->

<script lang="ts">
    import { createEventDispatcher } from 'svelte';

    let nsecKey = '';
    let nip07Key = 'nip07';
    const dispatch = createEventDispatcher();

    function submitNSEC() {
        if (nsecKey.trim()) {
            dispatch('submit', { key: nsecKey, method: 'nsec' });
        }
    }

    function submitNIP07() {
        if (nip07Key.trim()) {
            dispatch('submit', { key: nip07Key, method: 'nip07' });
        }
    }
</script>

<div class="login-container">
    <div class="login-option">
        <h2>NSEC Key</h2>
        <input type="text" bind:value={nsecKey} placeholder="Enter NSEC Key" />
        <button on:click={submitNSEC}>Login with NSEC</button>
    </div>
    <div class="login-option">
        <h2>NIP-07 Extension</h2>
        <!-- <input type="text" bind:value={nip07Key} placeholder="Enter NIP-07 Key" /> -->
        <button on:click={submitNIP07}>Login with NIP-07</button>
    </div>
</div>

<style>
    .login-container {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        gap: 1rem;
        padding: 1rem;
        border-radius: 1rem;
        width: 90%;
    }

    .login-option {
        background: #ffffff;
        border-radius: 1rem;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    h2 {
        color: #333;
        margin-bottom: 2rem;
    }

    input, button {
        width: 100%;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid var(--separator-line-color);
    }

    button {
        background-color: var(--logo-color);
        color: white;
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    button:hover {
        background-color: var(--logo-color-hover);
    }

	input {
		color: #333;
	}
</style>
