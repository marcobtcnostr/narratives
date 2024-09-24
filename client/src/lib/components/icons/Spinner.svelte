<!-- src\lib\components\icons\Spinner.svelte -->

<script lang="ts">
    // No script needed for a basic spinner
</script>

<div class="spinner"></div>

<style>
    .spinner {
        border: 4px solid rgba(0, 0, 0, 0.1);
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border-left-color: var(--logo-color);
        animation: spin 1s ease infinite;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
</style>
