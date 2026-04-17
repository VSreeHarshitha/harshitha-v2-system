export default defineConfig({
  server: {
    port: 3000,
    host: true, // This is the secret sauce for Docker!
    watch: {
      usePolling: true, // Needed for Windows E: drive sync
    },
  },
  // ... rest of your config
})