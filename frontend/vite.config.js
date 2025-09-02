import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  root: '.',          // le build part de la racine du frontend
  base: './',          // permet à Render de servir les fichiers correctement
  build: {
    outDir: 'dist',    // dossier de build final
    emptyOutDir: true
  }
});
